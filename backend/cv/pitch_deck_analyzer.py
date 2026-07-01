import cv2
import numpy as np
import os
from pdf2image import convert_from_path

class PitchDeckAnalyzer:
    def __init__(self):
        pass
        
    def analyze_pdf(self, pdf_path):
        """Analyzes a PDF pitch deck and returns scores."""
        try:
            # Convert PDF to list of images
            images = convert_from_path(pdf_path, dpi=150)
            if not images:
                return {"error": "Could not extract images from PDF."}
                
            results = []
            for i, img in enumerate(images):
                # Convert PIL image to OpenCV format (numpy array)
                cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                metrics = self.analyze_image(cv_img)
                metrics['page'] = i + 1
                results.append(metrics)
                
            # Aggregate results
            return self._aggregate_results(results)
        except Exception as e:
            return {"error": str(e)}

    def analyze_image(self, img):
        """Analyzes a single slide image."""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 1. Text Density (Approximation via thresholding)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        non_zero_pixels = cv2.countNonZero(thresh)
        total_pixels = img.shape[0] * img.shape[1]
        text_density = (non_zero_pixels / total_pixels) * 100
        
        # 2. Clutter Detection (via Edge density)
        edges = cv2.Canny(gray, 100, 200)
        edge_density = (cv2.countNonZero(edges) / total_pixels) * 100
        
        # 3. Visual Balance (Checking symmetry)
        left_half = gray[:, :img.shape[1]//2]
        right_half = gray[:, img.shape[1]//2:]
        left_weight = np.sum(left_half)
        right_weight = np.sum(right_half)
        balance_ratio = min(left_weight, right_weight) / max(left_weight, right_weight) if max(left_weight, right_weight) > 0 else 1
        
        # 4. Chart/Image Presence (Contours)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        large_contours = [c for c in contours if cv2.contourArea(c) > (total_pixels * 0.05)]
        has_visuals = len(large_contours) > 0
        
        return {
            "text_density": text_density,
            "edge_density": edge_density,
            "balance": balance_ratio,
            "has_visuals": has_visuals
        }
        
    def _aggregate_results(self, page_results):
        num_pages = len(page_results)
        if num_pages == 0:
            return {"error": "No pages to analyze."}
            
        avg_text_density = sum([p['text_density'] for p in page_results]) / num_pages
        avg_edge_density = sum([p['edge_density'] for p in page_results]) / num_pages
        avg_balance = sum([p['balance'] for p in page_results]) / num_pages
        pages_with_visuals = sum([1 for p in page_results if p['has_visuals']])
        visuals_ratio = pages_with_visuals / num_pages
        
        # Scoring logic (1-100)
        # Optimal text density is around 5-15%
        if avg_text_density > 20:
            text_score = 40
        elif avg_text_density < 2:
            text_score = 50
        else:
            text_score = 90
            
        # Clutter score
        clutter_score = max(0, 100 - (avg_edge_density * 5))
        
        # Visual design score
        visual_score = (avg_balance * 50) + (visuals_ratio * 50)
        
        # Overall quality
        overall_score = (text_score * 0.4) + (clutter_score * 0.3) + (visual_score * 0.3)
        
        recommendations = []
        if avg_text_density > 15:
            recommendations.append("Reduce text density on slides. Consider using bullet points and larger fonts.")
        if clutter_score < 60:
            recommendations.append("Slides appear cluttered. Increase white space to improve readability.")
        if visuals_ratio < 0.5:
            recommendations.append("Add more supporting graphs, charts, or images to illustrate key points.")
        if avg_balance < 0.7:
            recommendations.append("Improve visual hierarchy and layout symmetry on your slides.")
            
        if not recommendations:
            recommendations.append("Great job! Your pitch deck is well-balanced and visually appealing.")
            
        return {
            "total_pages": num_pages,
            "metrics": {
                "average_text_density": round(avg_text_density, 2),
                "average_clutter_index": round(avg_edge_density, 2),
                "visual_balance": round(avg_balance, 2),
                "visuals_ratio": round(visuals_ratio, 2)
            },
            "scores": {
                "quality_score": round(overall_score, 1),
                "visual_design_score": round(visual_score, 1),
                "investor_readiness_score": round((overall_score + visual_score) / 2, 1)
            },
            "recommendations": recommendations,
            "pages": page_results
        }

if __name__ == '__main__':
    analyzer = PitchDeckAnalyzer()
    # Dummy test if needed
    print("Pitch Deck Analyzer initialized.")
