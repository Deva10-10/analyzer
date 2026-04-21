# analyzer/app/views.py  ← REPLACE your existing views.py with this

import json

from urllib3 import request
from .services.ai_service import generate_ai_response
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
import ast


from .models import ChatHistory, RequirementAnalysis


# ══════════════════════════════════════════════
#  AI HELPER  ← REPLACE THIS WITH YOUR REAL API
# ══════════════════════════════════════════════
# def GEMINI_API_KEY(prompt: str) -> str:
#     import google.generativeai as genai
#     genai.configure(api_key="123")
#     model = genai.GenerativeModel("gemini-pro")
#     return model.generate_content(prompt).text
def generate_ai_response(prompt):
    import google.generativeai as genai
    
    genai.configure(api_key="AIzaSyBJBWNthlPDDB_0hprLfrXRgGe3k6w6bNc")
    model = genai.GenerativeModel("gemini-3-flash-preview")
    
    response = model.generate_content(prompt)
    return response.text
    
    """
    Swap this stub with your actual Gemini / OpenAI call.

    Example using google-generativeai:
    ─────────────────────────────────
        import google.generativeai as genai
        genai.configure(api_key="YOUR_GEMINI_API_KEY")
        model = genai.GenerativeModel("gemini-pro")
        return model.generate_content(prompt).text

    Example using openai:
    ─────────────────────
        import openai
        openai.api_key = "YOUR_KEY"
        r = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}]
        )
        return r.choices[0].message.content
    """
    return json.dumps({
        "problem_statement": "AI response placeholder — connect your AI API key.",
        "features": "1. Feature A\n2. Feature B\n3. Feature C",
        "user_stories": "As a user, I want to...",
        "tech_stack": "Django, React, PostgreSQL, Redis",
        "risks": "1. Market risk\n2. Technical risk",
        "mvp_scope": "Core features for MVP",
        "future_scope": "V2 features",
        "clarity_score": 7,
        "risk_level": "Medium",
        "feedback": "Your idea has good clarity.",
        "suggestions": "Consider narrowing your target market.",
        "breakdown": [
            {"label": "Problem Clarity", "score": 8},
            {"label": "Solution Fit", "score": 7},
            {"label": "Market Understanding", "score": 6},
            {"label": "Competitive Awareness", "score": 6}
        ],
        "revenue_text": "Subscription model recommended.",
        "revenue_models": [
            {"name": "SaaS Subscription", "description": "Monthly/yearly plans", "fit": "Best Fit"},
            {"name": "Freemium", "description": "Free tier with paid upgrades", "fit": "Good Fit"}
        ],
        "competitor_text": "Several players in this space.",
        "competitors": [
            {"name": "Competitor A", "description": "Similar product", "type": "Direct"},
            {"name": "Competitor B", "description": "Partial overlap", "type": "Indirect"}
        ],
        "market_analysis": "Growing market with high demand.",
        "total_cost": "₹8,00,000 – ₹15,00,000",
        "cost_range": "₹8L – ₹15L",
        "dev_cost": "₹6,00,000 – ₹10,00,000",
        "server_cost": "₹5,000/month",
        "api_cost": "₹2,000/month",
        "timeline": "3–4 months",
        "breakdown": [
            {"component": "Frontend Development", "cost": "₹2,00,000", "percent": 25},
            {"component": "Backend Development", "cost": "₹3,00,000", "percent": 37},
            {"component": "Database & Infra", "cost": "₹1,00,000", "percent": 13},
            {"component": "Design & UI", "cost": "₹1,50,000", "percent": 18},
            {"component": "Testing & QA", "cost": "₹50,000", "percent": 7}
        ],
        "assumptions": [
            {"key": "Developer rate", "value": "₹800–1500/hour"},
            {"key": "Hosting", "value": "AWS / GCP"}
        ],
        "notes": "Use cloud hosting with auto-scaling. Start with managed DB.",
        "total_duration": "6 months",
        "phases": [
            {"name": "Foundation", "duration": "Month 1–2", "percent": 33,
             "tasks": ["Setup project", "Auth system", "Core DB schema"],
             "milestones": ["Backend ready", "Auth working"]},
            {"name": "Core Features", "duration": "Month 2–4", "percent": 34,
             "tasks": ["Main feature development", "API integration", "Basic UI"],
             "milestones": ["MVP complete"]},
            {"name": "Launch Prep", "duration": "Month 5–6", "percent": 33,
             "tasks": ["Testing", "Performance optimization", "Launch"],
             "milestones": ["Beta launch", "Public launch"]}
        ],
        "launch_checklist": [
            "Set up production server",
            "Configure SSL certificate",
            "Set up monitoring (Sentry/Datadog)",
            "Write user documentation",
            "Set up analytics (Mixpanel/GA)",
            "Create landing page",
            "Set up email notifications",
            "Backup & disaster recovery plan"
        ]
    })


# ══════════════════════════
#  AUTH
# ══════════════════════════

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username", "").strip(),
            password=request.POST.get("password", "")
        )
        if user:
            login(request, user)
            return redirect("dashboard")
        return render(request, "login.html", {"error": "Invalid username or password."})
    return render(request, "login.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        username  = request.POST.get("username", "").strip()
        email     = request.POST.get("email", "").strip()
        pw1       = request.POST.get("password1", "")
        pw2       = request.POST.get("password2", "")
        fname     = request.POST.get("first_name", "").strip()
        lname     = request.POST.get("last_name", "").strip()

        if pw1 != pw2:
            return render(request, "register.html", {"error": "Passwords do not match."})
        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already taken."})

        user = User.objects.create_user(username=username, email=email, password=pw1,
                                        first_name=fname, last_name=lname)
        login(request, user)
        return redirect("dashboard")
    return render(request, "register.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You've been logged out.")
    return redirect("login")


# ══════════════════════════
#  DASHBOARD
# ══════════════════════════

@login_required(login_url="login")
def dashboard(request):
    analyses = RequirementAnalysis.objects.filter(user=request.user)
    return render(request, "dashboard.html", {
        "total_analyses":  analyses.count(),
        "total_chats":     ChatHistory.objects.filter(user=request.user).count(),
        "total_roadmaps":  0,
        "recent_analyses": analyses.order_by("-created_at")[:5],
    })


# ══════════════════════════
#  FEATURE 1 — REQUIREMENTS
# ══════════════════════════

@login_required(login_url="login")
def risk_analysis(request):
    past = RequirementAnalysis.objects.filter(user=request.user).order_by("-created_at")[:8]

    if request.method == "POST":
        idea     = request.POST.get("startup_idea", "").strip()
        industry = request.POST.get("industry", "")

        # Handle PDF upload (uncomment and install pdfplumber)
        # if request.FILES.get("pdf_file"):
        #     import pdfplumber
        #     with pdfplumber.open(request.FILES["pdf_file"]) as pdf:
        #         idea = "\n".join(p.extract_text() or "" for p in pdf.pages)

        if not idea:
            messages.error(request, "Please enter your startup idea.")
            return render(request, "risk_analysis.html", {"past_analyses": past})
        prompt = f"""
Analyze this startup idea.

Return response in STRICT JSON.
Use Markdown bullet format for:
- features
- user_stories
- risks

Industry: {industry}
Startup Idea: {idea}

Keys:
problem_statement (short paragraph),
features (markdown bullet list),
user_stories (markdown bullet list),
tech_stack (comma separated),
risks (markdown bullet list),
mvp_scope (short paragraph),
future_scope (short paragraph)

Example features format:
- User authentication
- Dashboard
- Payment integration
"""
#         prompt = f"""Analyze this startup idea and return ONLY valid JSON (no markdown, no backticks):
# Industry: {industry}
# Startup Idea: {idea}
# Keys needed: problem_statement, features (numbered list), user_stories (5 stories), tech_stack (comma-separated), risks (4-6 risks), mvp_scope, future_scope"""

        try:
            raw = generate_ai_response(prompt)
            try:
                data = json.loads(raw)
            except Exception:
                data = {"problem_statement": idea, "features": raw,
                        "user_stories": "", "tech_stack": "", "risks": "",
                        "mvp_scope": "", "future_scope": ""}

            analysis = RequirementAnalysis.objects.create(
                user=request.user, startup_idea=idea,
                problem_statement=data.get("problem_statement", idea),
                features=data.get("features", ""),
                user_stories=data.get("user_stories", ""),
                tech_stack=data.get("tech_stack", ""),
                risks=data.get("risks", ""),
                mvp_scope=data.get("mvp_scope", ""),
                future_scope=data.get("future_scope", ""),
                risk_analysis=data.get("risk_analysis", ""),
            )
            return render(request, "risk_analysis.html", {
                "result": analysis,
                "past_analyses": RequirementAnalysis.objects.filter(user=request.user).order_by("-created_at")[:8],
                "startup_idea": idea,
            })
        except Exception as e:
            messages.error(request, f"AI analysis failed: {str(e)}")

    return render(request, "risk_analysis.html", {"past_analyses": past})


@login_required(login_url="login")
def risk_detail(request, analysis_id):
    analysis = get_object_or_404(RequirementAnalysis, id=analysis_id, user=request.user)
    return render(request, "risk_detail.html", {"analysis": analysis})


# ══════════════════════════
#  FEATURE 2 — CLARITY SCORE
# ══════════════════════════

@login_required(login_url="login")
def idea_clarity(request):
    if request.method == "POST":
        ps   = request.POST.get("problem_statement", "").strip()
        ta   = request.POST.get("target_audience", "").strip()
        sol  = request.POST.get("solution", "").strip()
        alt  = request.POST.get("alternatives", "").strip()

        prompt = f"""Score this startup idea. Return ONLY valid JSON:
Problem: {ps} | Audience: {ta} | Solution: {sol} | Alternatives: {alt}
Keys: clarity_score (1-10), risk_level (Low/Medium/High), feedback, suggestions,
breakdown: [{{"label":"Problem Clarity","score":N}}, {{"label":"Solution Fit","score":N}},
{{"label":"Market Understanding","score":N}}, {{"label":"Competitive Awareness","score":N}}]"""

        try:
            raw = generate_ai_response(prompt)
            try:
                result = json.loads(raw)
            except Exception:
                result = {"clarity_score": 5, "risk_level": "Medium", "feedback": raw, "suggestions": ""}

            return render(request, "idea_clarity.html", {
                "result": result, "problem_statement": ps,
                "target_audience": ta, "solution": sol, "alternatives": alt,
            })
        except Exception as e:
            messages.error(request, f"Analysis failed: {str(e)}")

    return render(request, "idea_clarity.html")


# ══════════════════════════
#  FEATURE 3 — BUSINESS MODEL
# ══════════════════════════

@login_required(login_url="login")
def business_model(request):
    if request.method == "POST":
        idea  = request.POST.get("idea", "").strip()
        tm    = request.POST.get("target_market", "").strip()
        ind   = request.POST.get("industry", "").strip()
        uvp   = request.POST.get("uvp", "").strip()

        prompt = f"""Analyze business model. Return ONLY valid JSON:
Idea: {idea} | Market: {tm} | Industry: {ind} | UVP: {uvp}
Keys: revenue_models:[{{name,description,fit}}], competitors:[{{name,description,type(Direct/Indirect)}}], market_analysis"""

        try:
            raw = generate_ai_response(prompt)
            try:
                result = json.loads(raw)
            except Exception:
                result = {"revenue_text": raw, "competitor_text": ""}

            return render(request, "business_model.html", {
                "result": result, "idea": idea,
                "target_market": tm, "industry": ind, "uvp": uvp,
            })
        except Exception as e:
            messages.error(request, f"Analysis failed: {str(e)}")

    return render(request, "business_model.html")


# ══════════════════════════
#  FEATURE 4 — COST ESTIMATOR
# ══════════════════════════

@login_required(login_url="login")
def cost_estimator(request):
    if request.method == "POST":
        desc  = request.POST.get("project_description", "").strip()
        ptype = request.POST.get("project_type", "")
        tloc  = request.POST.get("team_location", "india")
        users = request.POST.get("expected_users", "small")
        ai_f  = request.POST.get("ai_features", "none")

        prompt = f"""Estimate project costs. Return ONLY valid JSON:
Description: {desc} | Type: {ptype} | Team location: {tloc} | Users: {users} | AI features: {ai_f}
Keys: total_cost, cost_range, dev_cost, server_cost, api_cost, timeline,
breakdown:[{{component,cost,percent}}], assumptions:[{{key,value}}], notes"""

        try:
            raw = generate_ai_response(prompt)
            try:
                result = json.loads(raw)
            except Exception:
                result = {"total_cost": "—", "dev_cost": "—", "server_cost": "—",
                          "api_cost": "—", "timeline": "—", "notes": raw}

            return render(request, "cost_estimator.html", {
                "result": result, "project_description": desc,
            })
        except Exception as e:
            messages.error(request, f"Estimation failed: {str(e)}")

    return render(request, "cost_estimator.html")


# ══════════════════════════
#  FEATURE 5 — ROADMAP
# ══════════════════════════

@login_required(login_url="login")
def roadmap(request):
    if request.method == "POST":
        idea  = request.POST.get("startup_idea", "").strip()
        feats = request.POST.get("features", "").strip()
        tsize = request.POST.get("team_size", "small")
        tline = request.POST.get("timeline", "6mo")
        meth  = request.POST.get("methodology", "agile")

        prompt = f"""Create product roadmap. Return ONLY valid JSON:
Product: {idea} | Features: {feats} | Team: {tsize} | Timeline: {tline} | Method: {meth}
Keys: total_duration, phases:[{{name,duration,percent,tasks:[],milestones:[]}}], launch_checklist:[]"""

        try:
            raw = generate_ai_response(prompt)
            try:
                result = json.loads(raw)
            except Exception:
                result = {"roadmap_text": raw, "phases": []}

            return render(request, "roadmap.html", {
                "result": result, "startup_idea": idea, "features": feats,
            })
        except Exception as e:
            messages.error(request, f"Roadmap failed: {str(e)}")

    return render(request, "roadmap.html")


# ══════════════════════════
#  CHATBOT
# ══════════════════════════

@login_required(login_url="login")
def chatbot(request):
    if request.GET.get("clear"):
        ChatHistory.objects.filter(user=request.user).delete()
        return redirect("chatbot")

    chats = ChatHistory.objects.filter(user=request.user).order_by("created_at")

    if request.method == "POST":
        user_input = request.POST.get("user_input", "").strip()
        if not user_input:
            return JsonResponse({"response": "Please enter a message."})

        prompt = f"""You are RequireAI, an expert AI startup consultant.
Help with: requirements, product strategy, tech stack, business models, MVP scoping, fundraising, growth.
Be concise and practical.

Question: {user_input}"""

        try:
            bot_response = generate_ai_response(prompt)
            # If response is JSON (from stub), convert to string
            if bot_response.startswith('{'):
                bot_response = "I'm ready to help! Please connect your AI API key in views.py to get real responses."
        except Exception as e:
            bot_response = f"Error: {str(e)}"

        ChatHistory.objects.create(
            user=request.user,
            user_message=user_input,
            bot_response=bot_response,
        )
        return JsonResponse({"response": bot_response})

    return render(request, "chatbot.html", {"chats": chats})


# ══════════════════════════
#  UTILITIES
# ══════════════════════════

@login_required(login_url="login")
def delete_chat(request, chat_id):
    get_object_or_404(ChatHistory, id=chat_id, user=request.user).delete()
    messages.success(request, "Chat deleted.")
    return redirect("chatbot")


@login_required(login_url="login")
def download_chat(request, chat_id):
    chat = get_object_or_404(ChatHistory, id=chat_id, user=request.user)
    content = f"You: {chat.user_message}\n\nAI: {chat.bot_response}\n\nDate: {chat.created_at}"
    response = HttpResponse(content, content_type="text/plain")
    response["Content-Disposition"] = f'attachment; filename="chat_{chat_id}.txt"'
    return response
