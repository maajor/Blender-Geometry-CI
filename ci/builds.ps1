$files = Get-Content .\geomanifest.json | ConvertFrom-Json
$tests = Get-ChildItem -Path .\builds\* -Include build*.py
foreach ($t in $tests.name)
{
    foreach ($f in $files.filename)
    {
        docker run --rm -v ${pwd}:/media/ nytimes/blender blender --background -P media/bpy_runner.py -- --script media/builds/$t --filename media/$f
    }
}