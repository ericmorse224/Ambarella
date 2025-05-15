Write-Host "Replacing ***REMOVED*** with } in source files..."

# Define extensions to scan
$extensions = @(".md", ".log", ".json", ".js", ".jsx", ".ts", ".tsx", ".py", ".txt")

# Find and process matching files
Get-ChildItem -Path . -Recurse -File | Where-Object {
    $extensions -contains $_.Extension
} | ForEach-Object {
    $path = $_.FullName
    Write-Host "Fixing $path"
    (Get-Content $path -Raw) -replace "\*\*\*REMOVED\*\*\*", "}" | Set-Content $path
}

Write-Host "Replacement complete. You can now commit and push your changes."
