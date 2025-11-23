ShopLite API - Docker and CI/CD Instructions

Running the API in Docker locally
1. Ensure Docker Desktop is installed and running.
2. Build the Docker image:
   docker build -t shoplite-api .
3. Run the Docker container:
   docker run -d -p 5000:5000 --name shoplite-api-container shoplite-api
4. Access the API at http://localhost:5000/

GitHub CI/CD Workflow
- The GitHub Actions workflow is located at `.github/workflows/ci-cd.yml`.
- This workflow runs on push or PR to the 'main' branch.
- It builds the Docker image, runs it to verify container startup, then stops and cleans up.
- To enable pushing Docker images to Docker Hub, add your Docker Hub credentials as GitHub secrets named DOCKER_USERNAME and DOCKER_PASSWORD.

Pushing to GitHub
1. Initialize git and commit all files:
   git init
   git add .
   git commit -m "Add Docker and CI/CD workflow"
2. Create a new GitHub repository and push your code:
   git remote add origin https://github.com/your-username/shoplite-api.git
   git push -u origin main

Adding collaborators
- Add user 'maescriba' as a collaborator on the GitHub repository through the repository settings page.

Viewing CI/CD Workflow on GitHub
- After pushing your code to GitHub, navigate to your repository page.
- Click on the "Actions" tab near the top of the page.
- In the Actions tab, you will see the list of workflow runs triggered by pushes or pull requests.
- Click on the latest run to see detailed logs and status for each job and step.
- Logs will show Docker build, container run, and any errors or success messages.
- This allows monitoring of your CI/CD pipeline run on GitHub.

Screenshots
- Take a screenshot of the API running in Docker (e.g., curl or browser hitting localhost:5000).
- Take a screenshot of GitHub Actions workflow showing a successful run.


