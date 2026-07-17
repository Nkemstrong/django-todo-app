from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegisterForm, TaskForm
from .models import Task


# ==========================================
# Register
# ==========================================

def register_view(request):

    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in.")
        return redirect("home")

    form = RegisterForm()

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")

            user = authenticate(
                request,
                username=username,
                password=password,
            )

            if user:
                login(request, user)
                messages.success(
                    request,
                    "Account created successfully."
                )
                return redirect("home")

        else:

            messages.error(
                request,
                "Please correct the errors below."
            )

    context = {
        "form": form,
    }

    return render(request, "register.html", context)


# ==========================================
# Login
# ==========================================

def login_view(request):

    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user:

            login(request, user)
            messages.success(request, "Login successful.")

            return redirect("home")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(request, "login.html")


# ==========================================
# Logout
# ==========================================

def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out."
    )

    return redirect("login")


# ==========================================
# Home
# ==========================================

@login_required(login_url="login")
def home(request):

    hour = datetime.now().hour

    if hour < 12:
        greeting = "Good Morning"

    elif hour < 17:
        greeting = "Good Afternoon"

    else:
        greeting = "Good Evening"

    greeting = (
        f"{greeting}, "
        f"{request.user.first_name or request.user.username}"
    )

    tasks = Task.objects.filter(
        user=request.user
    ).order_by("-created_at")

    # Dashboard Statistics
    total_tasks = tasks.count()

    completed_tasks = tasks.filter(done=True).count()

    pending_tasks = tasks.filter(done=False).count()

    context = {
        "greeting": greeting,
        "tasks": tasks,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
    }

    return render(
        request,
        "home.html",
        context,
    )

# ==========================================
# Add Task
# ==========================================

@login_required(login_url="login")
def add_task(request):

    if request.method == "POST":

        form = TaskForm(request.POST)

        if form.is_valid():

            task = form.save(commit=False)

            task.user = request.user

            task.save()

            messages.success(
                request,
                "Task added successfully."
            )

        else:

            messages.error(
                request,
                "Unable to add task."
            )

    return redirect("home")


# ==========================================
# Filter Tasks
# ==========================================

@login_required(login_url="login")
def filter_tasks(request, foo):

    if foo == "true":

        tasks = Task.objects.filter(
            user=request.user,
            done=True,
        )

    elif foo == "false":

        tasks = Task.objects.filter(
            user=request.user,
            done=False,
        )

    else:

        tasks = Task.objects.filter(
            user=request.user,
        )

    tasks = tasks.order_by("-created_at")

    # Dashboard Statistics
    all_tasks = Task.objects.filter(user=request.user)

    total_tasks = all_tasks.count()

    completed_tasks = all_tasks.filter(done=True).count()

    pending_tasks = all_tasks.filter(done=False).count()

    context = {
        "tasks": tasks,
        "greeting": f"Welcome, {request.user.first_name or request.user.username}",
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
    }        

    return render(
        request,
        "home.html",
        context,
    )


# ==========================================
# Update Task
# ==========================================

@login_required(login_url="login")
def update_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user,
    )

    form = TaskForm(instance=task)

    if request.method == "POST":

        form = TaskForm(
            request.POST,
            instance=task,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Task updated successfully."
            )

            return redirect("home")

        messages.error(
            request,
            "Unable to update task."
        )

    context = {
        "form": form,
        "task": task,
    }

    return render(
        request,
        "update_task.html",
        context,
    )


# ==========================================
# Delete Task
# ==========================================

@login_required(login_url="login")
def delete_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user,
    )

    task.delete()

    messages.success(
        request,
        "Task deleted successfully."
    )

    return redirect("home")