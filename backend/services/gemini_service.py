import google.generativeai as genai
import os

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None

    def _generate(self, prompt):
        if not self.model:
            return "Gemini API Key not configured. This is a mock response."
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating content: {str(e)}"

    def generate_all_insights(self, startup_details):
        prompt = f"""
        Act as an expert Venture Capital Analyst and Startup Advisor. Analyze the following startup:
        {startup_details}
        
        Provide your comprehensive analysis strictly in JSON format with exactly the following 6 string keys containing Markdown content:
        "swot": A detailed SWOT analysis (Strengths, Weaknesses, Opportunities, Threats) using bullet points.
        "roadmap": A structured roadmap (Phase 1 to Phase 5) with milestones.
        "bmc": A Business Model Canvas using bullet points.
        "competitors": A competitor analysis identifying 3-5 competitors and identifying market gaps.
        "funding": A specific funding strategy recommendation with reasoning.
        "pitch": A compelling investor pitch (Elevator Pitch, Problem, Solution, Market, Revenue, Ask).
        
        Do not include any formatting markdown around the JSON block like ```json.
        """
        response_text = self._generate(prompt)
        try:
            import json
            clean_json = response_text.replace('```json', '').replace('```', '').strip()
            return json.loads(clean_json)
        except Exception as e:
            return {
                "swot": response_text if "Error" in response_text else f"Error parsing JSON: {str(e)}\n\n{response_text}",
                "roadmap": "Generation failed due to quota or parsing error.",
                "bmc": "Generation failed.",
                "competitors": "Generation failed.",
                "funding": "Generation failed.",
                "pitch": "Generation failed."
            }

    def chat(self, user_message, history_list, context=""):
        if not self.model:
            return "Error: Gemini model not initialized."
            
        system_prompt = f"You are VenturePilot's AI Co-Founder. You are helping a user with their startup idea. Context about their startup analysis: {context}"
        
        # Format history for Gemini chat format
        gemini_history = []
        for msg in history_list:
            role = 'model' if msg['role'] == 'assistant' else 'user'
            gemini_history.append({"role": role, "parts": [msg['content']]})
            
        try:
            chat_session = self.model.start_chat(history=gemini_history)
            response = chat_session.send_message(f"System Context: {system_prompt}\nUser: {user_message}")
            return response.text
        except Exception as e:
            return f"Error communicating with AI: {str(e)}"
