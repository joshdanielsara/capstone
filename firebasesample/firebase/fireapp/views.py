from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .firebase import database
from django.http import JsonResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.db.models import F, ExpressionWrapper, FloatField
from django.http import HttpResponse
from django.shortcuts import render

def create_entry(request):
    if request.method == 'POST':
        project_name = request.POST.get('projectname')
        budget = request.POST.get('budget')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        spent = request.POST.get('spent')
        title = request.POST.get('title')  # Retrieve the title from the form

        # Check if the title already exists in the database
        existing_entry = database.child('Data').child(title).get().val()
        if existing_entry:
            return HttpResponse('<script>alert("An entry with this title already exists."); window.location.href = "/";</script>')

        # If the title doesn't exist, add the new entry to Firebase
        new_entry_ref = database.child('Data').child(title).set({
            "project_name": project_name,
            "budget": budget,
            "start_date": start_date,
            "end_date": end_date,
            "spent": spent
        })
        return HttpResponse('<script>alert("Entry created successfully."); window.location.href = "/";</script>')  # Return a success message with a redirect
    else:
        # Render form to add new entry
        return render(request, 'projects.html')


def create_ldf(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        budget = request.POST.get('budget')
        date = request.POST.get('date')
        title = request.POST.get('title') 

        # Check if the title already exists in the database
        existing_entry = database.child('LDF').child(title).get().val()
        if existing_entry:
            return JsonResponse({'error': "An entry with this title already exists."})

        # If the title doesn't exist, add the new entry to Firebase
        new_entry_ref = database.child('LDF').child(title).set({
            "name": name,
            "budget": budget,
            "date": date
            
        }) 
        return JsonResponse({'success': True})  # Return a success JSON response
    else:
        # Render form to add new entry
        return render(request, 'edit_form.html')







def projects(request):
    # Retrieve query parameter
    search_query_entry = request.GET.get('q')

    # Initialize data list
    data_list_entry = []

    # Retrieve data for regular entries if search query is provided
    if search_query_entry:
        data_entry = database.child('Data').order_by_child('project_name').equal_to(search_query_entry).get().val()
        if data_entry:
            for key, value in data_entry.items():
                entry = value
                entry['key'] = key
                data_list_entry.append(entry)
    else:
        # Retrieve all regular entries if no search query is provided
        data_entry = database.child('Data').get().val()
        if data_entry:
            for key, value in data_entry.items():
                entry = value
                entry['key'] = key
                data_list_entry.append(entry)

    # Calculate utilization rate for each project
    for entry in data_list_entry:
        budget = int(entry.get('budget', 0))  # Convert budget to integer
        spent = int(entry.get('spent', 0))  # Convert spent to integer
        if budget > 0:
            entry['utilization_rate'] = (spent / budget) * 100
        else:
            entry['utilization_rate'] = 0

    # Render template with retrieved data
    return render(request, 'projects.html', {
        'data_list_entry': data_list_entry,
        'search_query_entry': search_query_entry,
    })





def edit_form(request):
    # Retrieve query parameter
    search_query_ldf = request.GET.get('w')

    # Initialize data list
    data_list_ldf = []

    # Retrieve data for LDF entries if search query is provided
    if search_query_ldf:
        data_ldf = database.child('LDF').order_by_child('name').equal_to(search_query_ldf).get().val()
        if data_ldf:
            for key, value in data_ldf.items():
                entry = value
                entry['key'] = key
                data_list_ldf.append(entry)
    else:
        # Retrieve all LDF entries if no search query is provided
        data_ldf = database.child('LDF').get().val()
        if data_ldf:
            for key, value in data_ldf.items():
                entry = value
                entry['key'] = key
                data_list_ldf.append(entry)

    # Render template with retrieved data
    return render(request, 'edit_form.html', {
        'data_list_ldf': data_list_ldf,
        'search_query_ldf': search_query_ldf,
    })


def update_entry(request, entry_key):
    if request.method == 'POST':
        # Handle form submission to update entry
        name = request.POST.get('projectname')
        budget = request.POST.get('budget')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        spent = request.POST.get('spent')
        title = request.POST.get('title')

        # Update entry in Firebase
        database.child('Data').child(entry_key).update({
            "project_name": name,
            "budget": budget,
            "start_date": start_date,
            "end_date": end_date,
            "spent": spent,
            "title": title
        })
        # Redirect back to the main page
        return redirect('projects')  
    else:
        try:
            # Retrieve entry data from Firebase
            entry = database.child('Data').child(entry_key).get().val()
            if entry:
                entry['key'] = entry_key  # Add key to entry dict
                # Render edit form with entry data
                return render(request, 'projects.html', {'entry': entry, 'entry_key': entry_key})
            else:
                return HttpResponse('<script>alert("Failed to retrieve entry."); window.location.href = "/";</script>')  # Return an error message with a redirect
        except Exception as e:
            return HttpResponse('<script>alert("Failed to retrieve entry."); window.location.href = "/";</script>')  # Return an error message with a redirect


            

 

def delete_entry(request, entry_key):
    if request.method == 'POST':
        # Delete entry from Firebase 
        database.child('Data').child(entry_key).remove()
    return redirect('projects')  # Redirect back to the main page






def update_ldf_entry(request, entry_key):
    if request.method == 'POST':
        name = request.POST.get('name')
        budget = request.POST.get('budget')
        start_date = request.POST.get('date')  # Assuming the field name is 'date' for LDF
        # Update entry in Firebase
        database.child('LDF').child(entry_key).update({
            "name": name,
            "budget": budget,
            "date": start_date,
        })
        return redirect('edit_form')  # Redirect back to the edit_form page
    else:
        # Handle GET request to render the form
        # Retrieve entry data from Firebase
        entry = database.child('LDF').child(entry_key).get().val()
        # Render edit form with entry data
        return render(request, 'edit_form.html', {'entry': entry, 'entry_key': entry_key})

def delete_ldf_entry(request, entry_key):
    if request.method == 'POST':
        # Delete entry from Firebase 
        database.child('LDF').child(entry_key).remove()
    return redirect('edit_form')  # Redirect back to the edit_form page




















































