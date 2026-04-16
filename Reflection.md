This module focused on connecting the existing database models to actual FastAPI endpoints and verifying them through manual and automated testing.

The biggest challenges I faced were:

understanding how Swagger bearer token authorization works
using the correct calc_id for read/update/delete requests
getting pytest working in the correct environment
resolving Docker, dependency, and Trivy security issues
handling package version conflicts while keeping the application working

What I learned from this module:

how protected FastAPI routes use authentication dependencies
how Pydantic validation affects response codes such as 400 and 422
how to run integration tests in Docker when local environments cause issues
how dependency version conflicts can affect both builds and security scans
how CI/CD pipelines help catch problems before deployment