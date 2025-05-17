@echo off
echo Running tests with coverage...

:: Run tests and collect coverage data
coverage run -m pytest

:: Show terminal summary
coverage report -m

:: Generate HTML coverage report
coverage html

echo.
echo Open htmlcov\index.html in your browser to view the coverage report.
