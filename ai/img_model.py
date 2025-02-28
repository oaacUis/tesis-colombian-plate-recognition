# img_model.py

import cv2
import numpy as np
from PIL import Image
from PIL.ImageQt import ImageQt
from PySide6.QtGui import QPixmap
from itertools import combinations
from sklearn.cluster import KMeans  # type: ignore
from shapely import LineString  # type: ignore


def sharpen_new(img):
    """
    Apply K-means clustering for color quantization to sharpen an image.

    Parameters:
    - img (np.ndarray): The input image.

    Returns:
    - np.ndarray: The sharpened image.
    """
    Z = img.reshape((-1, 3))
    Z = np.float32(Z)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 2
    ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)  # noqa
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((img.shape))
    return res2


def detect_edges(image, low_threshold=50, high_threshold=150):
    """
    Detects edges in the input image using the Canny edge detection algorithm.

    Parameters:
        image (numpy.ndarray): The input grayscale image where edges will be detected.
        low_threshold (int): Lower bound for the hysteresis thresholding in Canny.
        high_threshold (int): Upper bound for the hysteresis thresholding in Canny.

    Returns:
        numpy.ndarray: The binary image with detected edges.  # noqa
    """
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return cv2.Canny(image, low_threshold, high_threshold)


def enhance_edges(edges, kernel_size=3, iterations=1):
    """
    Enhances the continuity of edges using morphological operations.

    Parameters:
        edges (numpy.ndarray): Binary edge image from Canny or other edge detector.
        kernel_size (int): Size of the kernel for morphological operations.
        iterations (int): Number of iterations for morphological operations.

    Returns:
        numpy.ndarray: Image with enhanced edge continuity.  # noqa
    """
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    # Apply dilation to close small gaps in the edges
    dilated = cv2.dilate(edges, kernel, iterations=iterations)
    closed = cv2.morphologyEx(dilated,
                              cv2.MORPH_CLOSE,
                              kernel,
                              iterations=iterations)

    return closed


def apply_bilateral_filter(image, d=4, sigma_color=10, sigma_space=10):
    """
    Applies a bilateral filter to the input image to reduce noise while preserving edges.

    Parameters:
        image (numpy.ndarray): The input image to be filtered.
        d (int): Diameter of each pixel neighborhood that is used during filtering.
        sigma_color (float): Filter sigma in the color space. Larger values mean more colors in the neighborhood will be mixed.
        sigma_space (float): Filter sigma in the coordinate space. Larger values mean farther pixels will influence each other.

    Returns:
        numpy.ndarray: The denoised image with preserved edges.  # noqa
    """
    return cv2.bilateralFilter(image, d, sigma_color, sigma_space)


def apply_clahe(image, clip_limit=2.0, tile_grid_size=(8, 8)):
    """
    Applies CLAHE (Contrast Limited Adaptive Histogram Equalization) to improve local contrast.

    Parameters:
        image (numpy.ndarray): The input grayscale image for contrast enhancement.
        clip_limit (float): Threshold for contrast limiting.
        tile_grid_size (tuple): Size of grid for the histogram equalization. Smaller values give stronger contrast enhancement.

    Returns:
        numpy.ndarray: The contrast-enhanced image.  # noqa
    """
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    return clahe.apply(image)


def apply_sharpening(image):
    """
    Applies a sharpening filter to the input image to enhance edges and details.

    Parameters:
        image (numpy.ndarray): The input image to be sharpened.

    Returns:
        numpy.ndarray: The sharpened image with enhanced edges.  # noqa
    """

    sharpening_kernel = np.array([[0, -1, 0],
                                  [-1, 5, -1],
                                  [0, -1, 0]])

    return cv2.filter2D(image, -1, sharpening_kernel)


def apply_image_filters(image, bilateral=True, clahe=True, sharpening=True):
    if bilateral:
        image = apply_bilateral_filter(image)
    if clahe:
        image = apply_clahe(image)
    if sharpening:
        image = apply_sharpening(image)
    return image


def check_intersection(p1, p2, q1, q2):
    """
    Checks if two line segments (p1->p2 and q1->q2) intersect.

    Parameters:
        p1, p2 (tuple): Points defining the first line segment.
        q1, q2 (tuple): Points defining the second line segment.

    Returns:
        bool: True if the line segments intersect, False otherwise.
    """
    def normalize_vector(k1, k2):
        v = k2-k1
        magnitude = np.linalg.norm(v)
        return v/magnitude

    v1_norm = normalize_vector(np.array(p1), np.array(p2))
    v2_norm = normalize_vector(np.array(q1), np.array(q2))

    dot_prod = np.dot(v1_norm, v2_norm)

    th = 0.6
    if -1*th < dot_prod < th:
        return True
    else:
        return False


def find_intersection(p1, p2, p3, p4):

    line1 = LineString([p1, p2])
    line2 = LineString([p3, p4])

    intersection = line1.intersection(line2)

    if intersection.is_empty:
        return None
    else:
        return intersection.coords[0]


def detect_plate_corners_hough(edges, image_shape, rho=1, theta=np.pi/180, threshold=50, min_line_length=20, max_line_gap=15, min_dist_ratio=0.3):  # noqa
    """
    Detects the corners of a license plate using Hough Line Transform and checks minimum distance criteria.

    Parameters:
        edges (numpy.ndarray): Binary edge image from Canny or other edge detector.
        image_shape (tuple): Shape of the original image (height, width).
        rho (float): Distance resolution of the accumulator in pixels.
        theta (float): Angle resolution of the accumulator in radians.
        threshold (int): Minimum number of votes (intersections) needed to detect a line.
        min_line_length (int): Minimum length of a line to be considered.
        max_line_gap (int): Maximum gap between segments to link them as a single line.
        min_dist_ratio (float): Minimum required distance ratio for valid corners (e.g., 0.1 means 10% of image width/height).

    Returns:
        numpy.ndarray or None: Array of four corner points if valid, or None if criteria are not met.  # noqa
    """

    min_dist = min(image_shape[0], image_shape[1]) * min_dist_ratio

    lines = cv2.HoughLinesP(edges, rho=rho, theta=theta, threshold=threshold, minLineLength=min_dist, maxLineGap=max_line_gap)  # noqa
    if lines is None:
        return None

    intersections = []
    for line1, line2 in combinations(lines, 2):

        p1 = (line1[0][0], line1[0][1])
        p2 = (line1[0][2], line1[0][3])
        p3 = (line2[0][0], line2[0][1])
        p4 = (line2[0][2], line2[0][3])

        # Check if lines intersect and calculate intersection point
        if check_intersection(p1, p2, p3, p4):

            intersection = find_intersection(p1, p2, p3, p4)
            if intersection is None:
                continue
            px = intersection[0]
            py = intersection[1]
            intersections.append((int(px), int(py)))
        else:
            continue

    # Filter valid points within the image bounds
    intersections = [
        (x, y) for x, y in intersections
        if 0 <= x < image_shape[1] and 0 <= y < image_shape[0]
    ]

    # Check if we have at least 4 intersection points
    if len(intersections) < 4:
        return None

    # Check if the points are not too close to each other
    valid_corners = exclude_regions(list(intersections), image_shape)
    if valid_corners is None:
        return None

    corners_grouped = cluster_and_select_corners(valid_corners, num_clusters=4,
                                                 image_shape=image_shape)
    final_corners = order_points_clockwise(corners_grouped)

    return final_corners


def order_points_clockwise(points):
    # Compute the centroid
    cx = np.mean([p[0] for p in points])
    cy = np.mean([p[1] for p in points])
    # Sort points based on angle relative to the centroid
    return sorted(points, key=lambda p: np.arctan2(p[1] - cy, p[0] - cx))


def exclude_regions(points, image_shape):
    """
    Exclude points that fall within the central region of an image.

    This function takes a list of points and the shape of an image, and returns a list of points that do not fall within the central third of the image both horizontally and vertically.

    Parameters:
    points (list of tuples): A list of (x, y) coordinates representing points.
    image_shape (tuple): A tuple representing the shape of the image (height, width).

    Returns:
    list of tuples: A list of (x, y) coordinates representing points that are outside the central region of the image.  # noqa
    """

    x_len = image_shape[1]
    y_len = image_shape[0]

    valid_points = []
    for point in points:
        point_x = point[0]
        point_y = point[1]
        limit_x1 = x_len//3
        limit_x2 = x_len*2//3
        limit_y1 = y_len//3
        limit_y2 = y_len*2//3

    if not (limit_x1 < point_x < limit_x2 or limit_y1 < point_y < limit_y2):
        valid_points.append(point)

    return valid_points


def cluster_and_select_corners(points, num_clusters=4, image_shape=None):
    """
    Groups detected points into clusters and selects the centroids as vertices.

    Args:
        points (list of tuple): List of coordinates of the detected points.
        num_clusters (int): Number of clusters (usually 4).
        image_shape (tuple): Dimensions of the image (height, width).

    Returns:
        centroids (list of tuple): Coordinates of the cluster centroids.
    """
    if len(points) < num_clusters:
        return None

    points = np.array(points)

    if image_shape is not None:
        height, width = image_shape[:2]
        initial_centroids = np.array([
            [0, 0],          # Top-left corner
            [0, width],      # Top-right corner
            [height, 0],     # Bottom-left corner
            [height, width]  # Bottom-right corner
        ])
    else:
        raise ValueError("image_shape is required for clustering")

    kmeans = KMeans(n_clusters=num_clusters,
                    init=initial_centroids,
                    n_init=1, random_state=42)
    kmeans.fit(points)

    centroids = kmeans.cluster_centers_
    return centroids.astype(int).tolist()


def find_plate_corners(image, bilateral=True, clahe=True, sharpening=True, enhance_edges=False):  # noqa

    edges = detect_edges(apply_image_filters(image, bilateral, clahe, sharpening))  # noqa
    if enhance_edges:
        edges = enhance_edges(edges)

    plate_corners = detect_plate_corners_hough(edges, edges.shape)
    return plate_corners


def calculate_homography_and_warp(image, src_points=None):
    """
    Calculates the homography matrix and applies a perspective transformation to rectify the plate.

    Parameters:
        image (numpy.ndarray): The original image containing the distorted plate.
        src_points (numpy.ndarray): The four corner points of the detected plate in the image,
                                    in the order [top-left, top-right, bottom-right, bottom-left].

    Returns:
        numpy.ndarray: The perspective-corrected (rectified) image of the plate.  # noqa
    """
    src_points = find_plate_corners(image)

    if src_points is None:
        return image

    # Assume a standard rectangular size for the license plate 200x100 pixels
    width, height = image.shape[1], image.shape[0]
    dst_points = np.array([[width - 1, 0], [0, 0],
                           [0, height - 1], [width - 1, height - 1]],
                          dtype="float32")

    # Calculate the homography matrix
    H, _ = cv2.findHomography(src_points, np.array(order_points_clockwise(dst_points)))  # noqa

    # Apply the perspective transformation
    rectified_plate = cv2.warpPerspective(image, H, (width, height))

    return rectified_plate


def opencv_resize(image, ratio):
    """
        Resize an image by a given ratio using OpenCV.

        Parameters:
        - image (np.ndarray): The input image.
        - ratio (float): The scaling ratio.

        Returns:
        - np.ndarray: The resized image.
        """

    width = int(image.shape[1] * ratio)
    height = int(image.shape[0] * ratio)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)


def to_img_opencv(imgPIL):
    """
    Convert a PIL image to an OpenCV image.

    Parameters:
    - imgPIL (Image.Image): The PIL image.

    Returns:
    - np.ndarray: The OpenCV image.
    """

    i = np.array(imgPIL)
    red = i[:, :, 0].copy()
    i[:, :, 0] = i[:, :, 2].copy()
    i[:, :, 2] = red
    return i


def to_img_pil(imgOpenCV):
    """
      Convert an OpenCV image to a PIL image.

      Parameters:
      - imgOpenCV (np.ndarray): The OpenCV image.

      Returns:
      - Image.Image: The PIL image.
      """
    return Image.fromarray(cv2.cvtColor(imgOpenCV, cv2.COLOR_BGR2RGB))


def convert_cv_image_to_qt_image(self, cv_img):
    """
      Convert an OpenCV image to a Qt image.

      Parameters:
      - cv_img (np.ndarray): The OpenCV image.

      Returns:
      - QPixmap: The Qt image.
      """
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    PIL_image = Image.fromarray(rgb_image).convert('RGB')
    return QPixmap.fromImage(ImageQt(PIL_image))


def controller(img, brightness=250, contrast=150):
    """
     Adjust the brightness and contrast of an image.

     Parameters:
     - img (np.ndarray): The input image.
     - brightness (int): The brightness value.
     - contrast (int): The contrast value.

     Returns:
     - np.ndarray: The image with adjusted brightness and contrast.
     """
    brightness = int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))

    contrast = int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127))

    if brightness != 0:

        if brightness > 0:

            shadow = brightness

            max = 255

        else:

            shadow = 0
            max = 255 + brightness

        al_pha = (max - shadow) / 255
        ga_mma = shadow
        cal = cv2.addWeighted(img, al_pha,
                              img, 0, ga_mma)

    else:
        cal = img

    if contrast != 0:
        Alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast))
        Gamma = 127 * (1 - Alpha)
        cal = cv2.addWeighted(cal, Alpha, cal, 0, Gamma)

    return cal


text_font = cv2.FONT_HERSHEY_DUPLEX
colorss = (0, 0, 255)
text_font_scale = 2


def draw_fps(videoFrame, fps):
    """
       Draw FPS information on a video frame.

       Parameters:
       - videoFrame (np.ndarray): The video frame on which to draw the FPS.
       - fps (float): The FPS value to draw.
       """
    text = 'fps: ' + str(int(fps))

    rectangle_bgr = (0, 0, 0)
    text_offset_x = 50
    text_offset_y = 75
    (text_width, text_height) = cv2.getTextSize(text,
                                                text_font,
                                                text_font_scale,
                                                thickness=5)[0]
    box_coords = (
        (text_offset_x + 20, text_offset_y), (text_offset_x + text_width + 20, text_offset_y - text_height - 20))  # noqa

    cv2.rectangle(videoFrame,
                  box_coords[0], box_coords[1],
                  rectangle_bgr, cv2.FILLED)
    cv2.putText(videoFrame, text,
                box_coords[0],
                text_font, text_font_scale,
                color=(255, 0, 0), thickness=5)


def grayscale(image):
    """
        Convert an image to grayscale and apply noise removal
        and thickening of fonts.

        Parameters:
        - image (np.ndarray): The input color image.

        Returns:
        - np.ndarray: The processed grayscale image.
        """
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh, im_bw = cv2.threshold(gray_image, 210, 230, cv2.THRESH_BINARY)
    no_noise = noise_removal(im_bw)
    dilated_image = thick_font(no_noise)
    return dilated_image


def noise_removal(image):
    """
        Apply morphological operations to remove noise from an image.

        Parameters:
        - image (np.ndarray): The input image.

        Returns:
        - np.ndarray: The noise-removed image.
        """
    import numpy as np
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return (image)


def thin_font(image):
    """
       Apply erosion to make the font thinner in an image.

       Parameters:
       - image (np.ndarray): The input image.

       Returns:
       - np.ndarray: The image with a thinner font.
       """
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)


def thick_font(image):
    """
       Apply dilation to make the font thicker in an image.

       Parameters:
       - image (np.ndarray): The input image.

       Returns:
       - np.ndarray: The image with a thicker font.
       """
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)
