import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.cluster import KMeans
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont

# 设置字体以支持中文字符
font_path = "C:/Windows/Fonts/simsun.ttc"  # 选择一个支持中文的字体文件路径
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

def put_chinese_text(img, text, position, font_path, font_size, color):
    """
    在OpenCV图像上添加中文文字
    
    参数：
    img - OpenCV图像
    text - 要添加的中文文字
    position - 文字位置 (x, y)
    font_path - 字体文件路径
    font_size - 字体大小
    color - 文字颜色，BGR格式，如(0, 0, 255)表示红色
    
    返回：
    添加了文字的图像
    """
    # 转换图像从OpenCV格式（BGR）到PIL格式（RGB）
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    # 创建绘图对象
    draw = ImageDraw.Draw(img_pil)
    
    # 加载字体
    font = ImageFont.truetype(font_path, font_size)
    
    # 在图像上绘制文字
    draw.text(position, text, font=font, fill=(color[2], color[1], color[0]))
    
    # 转换回OpenCV格式
    img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    
    return img_cv

class TemplateMatchingDetector:
    """模板匹配针头检测器"""
    
    def __init__(self, template_size=20, match_threshold=0.7, distance_threshold=14, 
             specified_rows=None, specified_cols=None):
        """
        初始化检测器
        
        参数:
        template_size - 模板大小
        match_threshold - 匹配阈值（适中的阈值，平衡检测严格性和检测率）
        distance_threshold - 距离阈值(用于去重和缺失检测，适中的阈值)
        specified_rows - 手动指定的行数（优先于自动估计）
        specified_cols - 手动指定的列数（优先于自动估计）
        """
        self.template_size = template_size
        self.match_threshold = match_threshold
        self.distance_threshold = distance_threshold
        self.template = None
        self.specified_rows = specified_rows
        self.specified_cols = specified_cols
        
    def select_template_roi(self, image_path):
        """
        手动从图像上框选ROI作为模板
        
        参数:
        image_path - 图像文件路径
        
        返回:
        template - 选择的模板
        """
        # 读取图像
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"无法读取图像: {image_path}")
        
        # 创建窗口和提示信息
        window_name = "选择针头模板 - 拖动鼠标框选一个针头，按Enter确认，按c取消"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 1200, 800)
        
        # 添加中文提示
        img_with_text = image.copy()
        
        # 使用辅助函数添加中文提示
        img_with_text = put_chinese_text(
            img_with_text, 
            "请框选一个针头作为模板", 
            (50, 50), 
            font_path, 
            36, 
            (0, 0, 255)  # 红色
        )
        
        img_with_text = put_chinese_text(
            img_with_text, 
            "按Enter确认选择，按c取消", 
            (50, 100), 
            font_path, 
            36, 
            (0, 0, 255)  # 红色
        )
        
        # 使用ROI选择器
        roi = cv2.selectROI(window_name, img_with_text, False, False)
        
        # 关闭窗口
        cv2.destroyWindow(window_name)
        
        # 检查是否选择了区域
        if roi[2] == 0 or roi[3] == 0:
            print("未选择区域，请重试")
            return None
        
        # 提取选择的区域作为模板
        x, y, w, h = roi
        template = image[y:y+h, x:x+w]
        
        # 保存模板
        self.template = template
        print(f"已选择模板，尺寸: {template.shape[1]}x{template.shape[0]}")
        
        return template
        
    def detect(self, image):
        """
        使用模板匹配检测针头
        
        参数:
        image - 输入图像
        
        返回:
        detected_pins - 检测到的针头位置列表
        result_image - 标记了检测结果的图像
        """
        if self.template is None:
            print("未设置模板，请先使用select_template_roi方法选择模板")
            return [], image.copy()
        
        # 转换为灰度图
        if len(image.shape) > 2:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
            
        if len(self.template.shape) > 2:
            template = cv2.cvtColor(self.template, cv2.COLOR_BGR2GRAY)
        else:
            template = self.template.copy()
            
        # 存储检测结果
        detected_pins = []
        result_image = image.copy() if len(image.shape) > 2 else cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
        # 增强对比度
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced_gray = clahe.apply(gray)
        
        # 使用更多尺度进行模板匹配，以应对密集排列
        for scale in np.linspace(0.7, 1.3, 15):
            # 缩放模板
            w, h = template.shape[::-1]
            width = int(w * scale)
            height = int(h * scale)
            
            if width <= 0 or height <= 0:
                continue
                
            resized_template = cv2.resize(template, (width, height))
            
            # 对原始灰度图和增强后的图像都进行模板匹配
            images_to_match = [gray, enhanced_gray]
            
            for img in images_to_match:
                # 执行模板匹配
                res = cv2.matchTemplate(img, resized_template, cv2.TM_CCOEFF_NORMED)
                
                # 找出匹配位置
                loc = np.where(res >= self.match_threshold)
                
                points = list(zip(*loc[::-1]))  # 转换为坐标点列表
                
                # 添加到检测结果
                for pt in points:
                    x, y = pt
                    center_x = x + width // 2
                    center_y = y + height // 2
                    # 添加匹配分数
                    match_score = res[y, x]
                    detected_pins.append((center_x, center_y, scale, match_score))
        
        # 去除重复检测
        final_pins = self._remove_duplicates(detected_pins)
        
        # 在密集针头情况下，可能需要调整去重逻辑
        if self.specified_rows is not None and self.specified_cols is not None:
            # 如果预期针头数量远大于检测到的数量，可能需要降低去重标准
            expected_count = self.specified_rows * self.specified_cols
            if len(final_pins) < expected_count * 0.7:  # 检测到的针头少于预期的70%
                print(f"警告: 检测到的针头数量({len(final_pins)})远少于预期({expected_count})")
                print("尝试降低匹配阈值并重新检测...")
                
                # 可以考虑临时降低匹配阈值并重新检测
                original_threshold = self.match_threshold
                self.match_threshold = max(0.6, self.match_threshold - 0.1)
                
                # 清空之前的结果重新检测
                detected_pins = []
                
                # 重新进行模板匹配
                for scale in np.linspace(0.7, 1.3, 15):
                    w, h = template.shape[::-1]
                    width = int(w * scale)
                    height = int(h * scale)
                    
                    if width <= 0 or height <= 0:
                        continue
                        
                    resized_template = cv2.resize(template, (width, height))
                    
                    for img in images_to_match:
                        res = cv2.matchTemplate(img, resized_template, cv2.TM_CCOEFF_NORMED)
                        loc = np.where(res >= self.match_threshold)
                        points = list(zip(*loc[::-1]))
                        
                        for pt in points:
                            x, y = pt
                            center_x = x + width // 2
                            center_y = y + height // 2
                            match_score = res[y, x]
                            detected_pins.append((center_x, center_y, scale, match_score))
                
                # 使用更小的距离阈值去重
                temp_distance = self.distance_threshold
                self.distance_threshold = max(5, self.distance_threshold * 0.7)
                final_pins = self._remove_duplicates(detected_pins)
                
                # 恢复原始阈值
                self.match_threshold = original_threshold
                self.distance_threshold = temp_distance
        
        # 在图像上标记检测到的针头
        for pin in final_pins:
            x, y = pin[:2]
            cv2.circle(result_image, (int(x), int(y)), 5, (0, 255, 0), 2)
            
        return final_pins, result_image
        
    def _remove_duplicates(self, pins):
        """
        去除重复检测的针头
        
        参数:
        pins - 检测到的针头列表
        
        返回:
        final_pins - 去重后的针头列表
        """
        if not pins:
            return []
            
        # 按匹配得分排序，确保保留得分最高的点
        pins = sorted(pins, key=lambda x: x[3], reverse=True)
        
        # 转换为numpy数组以加速计算
        pins_array = np.array([(pin[0], pin[1]) for pin in pins])
        
        # 创建标记数组
        is_duplicate = np.zeros(len(pins), dtype=bool)
        
        # 使用更严格的去重逻辑
        for i in range(len(pins)):
            if is_duplicate[i]:
                continue
                
            # 计算当前点与所有其他点的距离
            current_point = pins_array[i]
            distances = np.sqrt(np.sum((pins_array - current_point) ** 2, axis=1))
            
            # 将当前点到自身的距离设置为无穷大，避免自我标记
            distances[i] = np.inf
            
            # 找出所有距离小于阈值的点
            close_points = distances < self.distance_threshold
            
            # 标记这些点为重复
            is_duplicate[close_points] = True
        
        # 保留未被标记为重复的点
        final_pins = [pin for i, pin in enumerate(pins) if not is_duplicate[i]]
        
        return final_pins
        
    def estimate_grid(self, pins):
        """
        估计模具针头网格的行列数
        
        参数:
        pins - 检测到的针头位置列表
        
        返回:
        num_rows - 估计的行数
        num_cols - 估计的列数
        """
        if len(pins) < 10:
            print("检测到的针头太少，无法可靠估计网格")
            return 0, 0
            
        # 提取x和y坐标
        x_coords = np.array([pin[0] for pin in pins]).reshape(-1, 1)
        y_coords = np.array([pin[1] for pin in pins]).reshape(-1, 1)
        
        # 使用KMeans聚类估计行列数
        max_clusters = min(40, len(pins) // 2)  # 防止聚类数过多
        
        # 估计列数(x坐标聚类)
        x_score = []
        x_labels = []
        
        for n_clusters in range(2, max_clusters):
            kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init=10).fit(x_coords)
            x_score.append(kmeans.inertia_)
            x_labels.append(kmeans.labels_)
            
        # 使用肘部法则找到最佳聚类数
        x_score = np.array(x_score)
        num_cols = self._find_elbow_point(range(2, max_clusters), x_score) + 2
        
        # 估计行数(y坐标聚类)
        y_score = []
        y_labels = []
        
        for n_clusters in range(2, max_clusters):
            kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init=10).fit(y_coords)
            y_score.append(kmeans.inertia_)
            y_labels.append(kmeans.labels_)
            
        # 使用肘部法则找到最佳聚类数
        y_score = np.array(y_score)
        num_rows = self._find_elbow_point(range(2, max_clusters), y_score) + 2
        
        return num_rows, num_cols
        
    def _find_elbow_point(self, x, y):
        """使用肘部法则找到最佳拐点"""
        # 计算曲线上每点的曲率
        n_points = len(x)
        if n_points <= 2:
            return 0
            
        # 归一化
        x_norm = (x - np.min(x)) / (np.max(x) - np.min(x))
        y_norm = (y - np.min(y)) / (np.max(y) - np.min(y))
        
        # 找到距离直线最远的点
        a = np.array([x_norm[0], y_norm[0]])
        b = np.array([x_norm[-1], y_norm[-1]])
        
        max_dist = 0
        elbow_idx = 0
        
        for i in range(1, n_points - 1):
            p = np.array([x_norm[i], y_norm[i]])
            
            # 计算点到直线的距离
            dist = np.abs(np.cross(p - a, b - a)) / np.linalg.norm(b - a)
            
            if dist > max_dist:
                max_dist = dist
                elbow_idx = i
                
        return elbow_idx
        
    def create_ideal_grid(self, image_shape, num_rows, num_cols, detected_pins=None):
        """
        创建理想针头网格
        
        参数:
        image_shape - 图像形状(高度, 宽度)
        num_rows - 行数
        num_cols - 列数
        detected_pins - 检测到的针头位置列表，用于校准网格
        
        返回:
        grid_pins - 理想网格点列表
        """
        height, width = image_shape[:2]
        
        if detected_pins and len(detected_pins) > 0:
            # 提取检测到的针头坐标
            detected_coords = np.array([pin[:2] for pin in detected_pins])
            
            # 使用百分位数而不是最大最小值，避免异常值的影响
            min_x = np.percentile(detected_coords[:, 0], 2)  # 使用第2百分位
            max_x = np.percentile(detected_coords[:, 0], 98)  # 使用第98百分位
            min_y = np.percentile(detected_coords[:, 1], 2)
            max_y = np.percentile(detected_coords[:, 1], 98)
            
            # 计算检测到的针头的平均间距
            sorted_x = np.sort(detected_coords[:, 0])
            sorted_y = np.sort(detected_coords[:, 1])
            x_diffs = np.diff(sorted_x)
            y_diffs = np.diff(sorted_y)
            avg_x_spacing = np.median(x_diffs)
            avg_y_spacing = np.median(y_diffs)
            
            # 使用平均间距的一半作为边距
            margin_x = avg_x_spacing / 2
            margin_y = avg_y_spacing / 2
            
            # 确保边距不会导致网格点超出图像范围
            min_x = max(min_x - margin_x, 0)
            max_x = min(max_x + margin_x, width)
            min_y = max(min_y - margin_y, 0)
            max_y = min(max_y + margin_y, height)
            
            # 计算间距
            col_spacing = (max_x - min_x) / (num_cols - 1)
            row_spacing = (max_y - min_y) / (num_rows - 1)
        else:
            # 如果没有检测到的针头，使用更小的默认边距
            margin_x = width * 0.02  # 减小默认边距
            margin_y = height * 0.02
            
            min_x = margin_x
            max_x = width - margin_x
            min_y = margin_y
            max_y = height - margin_y
            
            col_spacing = (max_x - min_x) / (num_cols - 1)
            row_spacing = (max_y - min_y) / (num_rows - 1)
        
        # 生成网格点
        grid_pins = []
        for row in range(num_rows):
            for col in range(num_cols):
                x = min_x + col * col_spacing
                y = min_y + row * row_spacing
                grid_pins.append((int(x), int(y)))
        
        return grid_pins
        
    def find_missing_pins(self, grid_pins, detected_pins):
        """
        找出缺失的针头
        
        参数:
        grid_pins - 理想网格点列表
        detected_pins - 检测到的针头位置列表
        
        返回:
        missing_pins - 缺失针头列表
        """
        if not grid_pins or not detected_pins:
            return []
            
        missing_pins = []
        matched_grid_pins = []
        matched_detected_pins = []
        
        # 使用kd树加速最近邻查找
        try:
            from scipy.spatial import cKDTree
            # 将检测到的针头坐标转换为numpy数组
            detected_coords = np.array([pin[:2] for pin in detected_pins])
            
            # 构建KD树
            tree = cKDTree(detected_coords)
            
            # 对于每个网格点，查找最近的检测点
            for grid_pin in grid_pins:
                dist, idx = tree.query(grid_pin, k=1)
                
                # 判断是否匹配
                if dist <= self.distance_threshold:
                    matched_grid_pins.append(grid_pin)
                    matched_detected_pins.append((detected_coords[idx][0], detected_coords[idx][1]))
                else:
                    missing_pins.append(grid_pin)
                    
        except ImportError:
            # 如果没有scipy，退回到原始方法
            print("未安装scipy，使用较慢的暴力匹配方法")
            
            for grid_pin in grid_pins:
                gx, gy = grid_pin
                matched = False
                best_dist = float('inf')
                best_pin = None
                
                for detected_pin in detected_pins:
                    dx, dy = detected_pin[:2]
                    dist = np.sqrt((gx - dx)**2 + (gy - dy)**2)
                    
                    if dist < best_dist:
                        best_dist = dist
                        best_pin = detected_pin
                
                if best_dist <= self.distance_threshold:
                    matched = True
                    matched_grid_pins.append(grid_pin)
                    matched_detected_pins.append((best_pin[0], best_pin[1]))
                    
                if not matched:
                    missing_pins.append(grid_pin)
        
        # 当缺失针头数量异常高时（超过30%），输出警告并提供建议
        if len(missing_pins) > len(grid_pins) * 0.3:
            print(f"警告: 缺失针头比例异常高 ({len(missing_pins)}/{len(grid_pins)}，{len(missing_pins)/len(grid_pins):.2%})")
            print("可能的原因:")
            print("1. 模板选择不当")
            print("2. 匹配阈值设置过高")
            print("3. 网格参数(行列数)设置不当")
            
            # 分析缺失位置分布是否有规律
            # 计算每一行和每一列的缺失数量
            if self.specified_rows is not None and self.specified_cols is not None:
                row_missing = [0] * self.specified_rows
                col_missing = [0] * self.specified_cols
                
                for gx, gy in missing_pins:
                    # 估计行列索引
                    col_idx = int(round((gx - grid_pins[0][0]) / ((grid_pins[-1][0] - grid_pins[0][0]) / (self.specified_cols - 1))))
                    row_idx = int(round((gy - grid_pins[0][1]) / ((grid_pins[-1][1] - grid_pins[0][1]) / (self.specified_rows - 1))))
                    
                    if 0 <= row_idx < self.specified_rows and 0 <= col_idx < self.specified_cols:
                        row_missing[row_idx] += 1
                        col_missing[col_idx] += 1
                
                # 检查是否有整行或整列缺失
                empty_rows = [i for i, count in enumerate(row_missing) if count > self.specified_cols * 0.8]
                empty_cols = [i for i, count in enumerate(col_missing) if count > self.specified_rows * 0.8]
                
                if empty_rows:
                    print(f"发现可能整行缺失: 行 {empty_rows}")
                    print("建议: 检查这些行的图像质量或调整行数设置")
                
                if empty_cols:
                    print(f"发现可能整列缺失: 列 {empty_cols}")
                    print("建议: 检查这些列的图像质量或调整列数设置")
        
        return missing_pins
        
    def process_image(self, image_path, output_dir=None, save_results=True):
        """
        处理模具图像，检测针头并分析缺失
        
        参数:
        image_path - 图像文件路径
        output_dir - 输出目录路径
        save_results - 是否保存结果图像
        
        返回:
        result_dict - 包含处理结果的字典
        """
        # 确保输出目录存在
        if save_results:
            if output_dir is None:
                output_dir = os.path.join(os.path.dirname(image_path), 'output')
            os.makedirs(output_dir, exist_ok=True)
            
        # 生成时间戳
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 读取图像
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"无法读取图像: {image_path}")
            
        # 保存原始图像
        if save_results:
            cv2.imwrite(os.path.join(output_dir, f'{timestamp}_1_original.jpg'), image)
            
        # 预处理图像
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 1. 初步去噪
        denoised = cv2.fastNlMeansDenoising(gray, None, h=10, templateWindowSize=7, searchWindowSize=21)
        
        # 2. 应用CLAHE增强对比度（分两次，更细致的增强）
        clahe1 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
        enhanced1 = clahe1.apply(denoised)
        clahe2 = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced2 = clahe2.apply(enhanced1)
        
        # 3. 使用Gamma校正增强暗部细节
        gamma = 1.2
        gamma_corrected = np.power(enhanced2 / 255.0, gamma) * 255.0
        gamma_corrected = gamma_corrected.astype(np.uint8)
        
        # 4. 应用自适应阈值处理
        adaptive_thresh = cv2.adaptiveThreshold(
            gamma_corrected,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )
        
        # 5. 形态学操作增强针头特征
        kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        
        # 开运算去除小噪点
        morph = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_OPEN, kernel_open)
        # 闭运算填充针头内部
        morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel_close)
        
        # 6. 边缘增强
        edge = cv2.Laplacian(gamma_corrected, cv2.CV_8U, ksize=3)
        enhanced_with_edges = cv2.addWeighted(gamma_corrected, 1.0, edge, 0.3, 0)
        
        # 7. 最终的预处理结果
        final_enhanced = cv2.addWeighted(enhanced_with_edges, 0.7, morph, 0.3, 0)
        
        # 8. 最后的平滑处理
        final_result = cv2.bilateralFilter(final_enhanced, d=5, sigmaColor=50, sigmaSpace=50)
        
        if save_results:
            # 保存增强后的图像
            cv2.imwrite(os.path.join(output_dir, f'{timestamp}_2_enhanced.jpg'), final_result)
            
        # 检查是否已设置模板
        if self.template is None:
            print("请先使用select_template_roi方法选择模板")
            # 提示用户手动选择模板
            self.select_template_roi(image_path)
        
        # 保存模板
        if self.template is not None and save_results:
            cv2.imwrite(os.path.join(output_dir, f'{timestamp}_3_template.jpg'), self.template)
                
        # 检测针头
        detected_pins, detection_image = self.detect(image)
        if save_results:
            cv2.imwrite(os.path.join(output_dir, f'{timestamp}_4_detected.jpg'), detection_image)
            
        # 确定行列数（优先使用手动指定的值）
        if self.specified_rows is not None and self.specified_cols is not None:
            num_rows, num_cols = self.specified_rows, self.specified_cols
            print(f"使用手动指定的网格大小: {num_rows}行 x {num_cols}列")
        else:
            # 估计网格
            estimated_rows, estimated_cols = self.estimate_grid(detected_pins)
            num_rows, num_cols = estimated_rows, estimated_cols
                
        print(f"使用的网格大小: {num_rows}行 x {num_cols}列")
        
        # 创建理想网格，传入检测到的针头位置
        grid_pins = self.create_ideal_grid(image.shape, num_rows, num_cols, detected_pins)
        
        # 绘制理想网格
        grid_image = image.copy()
        for x, y in grid_pins:
            cv2.circle(grid_image, (int(x), int(y)), 5, (255, 0, 0), 1)
            
        if save_results:
            cv2.imwrite(os.path.join(output_dir, f'{timestamp}_5_grid.jpg'), grid_image)
            
        # 找出缺失针头
        missing_pins = self.find_missing_pins(grid_pins, detected_pins)
        
        # 在图像上标记缺失针头
        result_image = detection_image.copy()
        
        for i, (x, y) in enumerate(missing_pins):
            # 使用红色十字标记缺失针头
            cv2.circle(result_image, (int(x), int(y)), 10, (0, 0, 255), 2)
            cv2.line(result_image, (int(x)-12, int(y)), (int(x)+12, int(y)), (0, 0, 255), 2)
            cv2.line(result_image, (int(x), int(y)-12), (int(x), int(y)+12), (0, 0, 255), 2)
            
        if save_results:
            cv2.imwrite(os.path.join(output_dir, f'{timestamp}_6_result.jpg'), result_image)
            
        # 打印统计信息
        total_pins = len(grid_pins)
        detected_count = len(detected_pins)
        missing_count = len(missing_pins)
        
        detection_rate = detected_count / total_pins if total_pins > 0 else 0
        defect_rate = missing_count / total_pins if total_pins > 0 else 0
        
        print(f"检测结果:")
        print(f"总针头数量: {total_pins}")
        print(f"检测到的针头数量: {detected_count}")
        print(f"缺失针头数量: {missing_count}")
        print(f"检测率: {detection_rate:.2%}")
        print(f"缺陷率: {defect_rate:.2%}")
        
        # 可视化结果
        if save_results:
            plt.figure(figsize=(15, 10))
            
            plt.subplot(231)
            plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            plt.title('原始图像')
            
            plt.subplot(232)
            plt.imshow(final_result, cmap='gray')
            plt.title('增强图像')
            
            if self.template is not None:
                plt.subplot(233)
                if len(self.template.shape) > 2:
                    plt.imshow(cv2.cvtColor(self.template, cv2.COLOR_BGR2RGB))
                else:
                    plt.imshow(self.template, cmap='gray')
                plt.title('针头模板')
            
            plt.subplot(234)
            plt.imshow(cv2.cvtColor(detection_image, cv2.COLOR_BGR2RGB))
            plt.title('检测结果')
            
            plt.subplot(235)
            plt.imshow(cv2.cvtColor(grid_image, cv2.COLOR_BGR2RGB))
            plt.title('理想网格')
            
            plt.subplot(236)
            plt.imshow(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB))
            plt.title(f'缺陷分析 ({defect_rate:.2%})')
            
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f'{timestamp}_7_分析汇总.jpg'), dpi=300)
            
        # 汇总结果
        result_dict = {
            'total_pins': total_pins,
            'detected_count': detected_count,
            'missing_count': missing_count,
            'detection_rate': detection_rate,
            'defect_rate': defect_rate,
            'detected_pins': detected_pins,
            'missing_pins': missing_pins,
            'grid_size': (num_rows, num_cols),
            'output_dir': output_dir if save_results else None,
            'timestamp': timestamp,
            'result_image': result_image
        }
        
        return result_dict

# 使用示例
if __name__ == "__main__":
    # 创建检测器实例
    detector = TemplateMatchingDetector(
        template_size=20,
        match_threshold=0.755,  # 提高匹配阈值，使模板匹配更严格
        distance_threshold=9,  # 略微减小距离阈值，避免相近点的误检
        specified_rows=31,  # 指定行数
        specified_cols=28   # 指定列数
    )
    
    # 使用示例：手动框选模板并检测
    image_path = "22.jpg"  # 替换为实际图像路径
    
    try:
        # 手动框选模板
        print("请在弹出窗口中框选一个针头作为模板")
        template = detector.select_template_roi(image_path)
        
        if template is not None:
            # 处理图像并输出结果
            results = detector.process_image(image_path)
            
            # 显示结果图像
            plt.figure(figsize=(10, 8))
            plt.imshow(cv2.cvtColor(results['result_image'], cv2.COLOR_BGR2RGB))
            plt.title(f"Detection Result - Defect Rate: {results['defect_rate']:.2%}")
            plt.show()
        else:
            print("未选择模板，无法进行检测")
        
    except Exception as e:
        print(f"处理图像时出错: {e}") 