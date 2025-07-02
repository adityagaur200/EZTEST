from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, FileResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from ShareApp.models import FileModel, UserProfile


@csrf_exempt
@login_required
def upload_files(request):
    if request.method == "POST":
        print("FILES:", request.FILES)
        uploaded_file = request.FILES.get('file')

        if not uploaded_file:
            return JsonResponse({'error': 'No file provided'}, status=400)

        print(f"Received file: {uploaded_file.name}")

        allowed_types = [
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        ]

        if uploaded_file.content_type not in allowed_types:
            return JsonResponse({'error': 'Invalid file type'}, status=400)

        # Save (assuming logged in user for now is user ID = 1 for testing)
        FileModel.objects.create(user=User.objects.get(id=1), file=uploaded_file)
        return JsonResponse({'message': 'File uploaded successfully'})

    return JsonResponse({'error': 'Only POST allowed'}, status=405)

@login_required
@csrf_exempt
def download_file(request, file_id):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return JsonResponse({'message': 'User profile not found'}, status=400)

    if user_profile.role != 'client':
        return JsonResponse({'message': 'Access denied: Only client users can download files'}, status=403)

    file = get_object_or_404(FileModel, id=file_id)

    # Build absolute download URL
    file_url = request.build_absolute_uri(file.file.url)

    return JsonResponse({
        "download-link": file_url,
        "message": "success"
    })

@csrf_exempt
@login_required
def all_files(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return JsonResponse({'message': 'User profile not found'}, status=400)

    if user_profile.role != 'client':
        return JsonResponse({'message': 'Access denied: Only client users can view files'}, status=403)

    files = FileModel.objects.all()
    files_data = [
        {
            'id': file.id,
            'filename': file.file.name,
            'uploaded_by': file.user.username,
            'uploaded_at': file.uploaded_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for file in files
    ]

    return JsonResponse({'files': files_data})
