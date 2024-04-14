import re
import os

paths = []
temp_directory = 'C:\\Users\\mbric\\Documents\\Sook\\sidec_org\\sidec\\templates'
for folder_name, subfolders, filenames in os.walk(temp_directory):
    print(f'The current folder is {folder_name}')
    for filename in filenames:
        file_path = os.path.join(folder_name, filename)
        if file_path.endswith('.html'):
            name = filename.replace('.html', '')
            full_thing = f"path('{name}', views.default, name='{name}'),"
            paths.append(full_thing)

print('\n'.join(paths))


# with open('', 'r+') as f:
#     old = f.read()
#     f.write('{% load static %}')
# print(re.sub('src="(?!.*\/\/)\W*(.*)"', 'src="{% static \'\\1\' %}"', tml))
# print(re.sub('link(.*)href="(?!.*\/\/)\W*(.*)"', 'link(\\1)href="{% static \'\\2\' %}"'))
# print(re.sub('(a|location)(.*)href=["\'](?!.*\/\/).*?(\w+)\.html', '\\1\\2href=\'{% url \'\\3\' %}', tml))