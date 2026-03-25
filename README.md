# Thematic Client SDK

Python SDK for the [Thematic](https://getthematic.com/) API. Provides a thin wrapper around the REST endpoints for authentication, data management, survey configuration, theme analysis, and more.

Requires Python 3.12.

## Installation

```bash
pip install .
```

For development:

```bash
uv sync
```

## Quick Start

### 1. Get a Refresh Token

Use the included CLI tool to generate a long-lived refresh token from your credentials:

```bash
thematic-client-auth
```

You will be prompted for your username, password, and integration name. Keep the resulting refresh token secure -- it can be used to access resources on your behalf.

Refresh tokens can be invalidated in the Thematic client UI or programmatically via the API. Once invalidated, they cannot be recovered.

### 2. Exchange for an Access Token

Access tokens are short-lived. Exchange your refresh token for one before each session:

```python
from thematic_client_sdk import Auth

auth = Auth()
access_token = auth.swap_refresh_token("your_refresh_token")
```

You can also authenticate directly with username/password (returns an access token without a refresh token):

```python
access_token = auth.login_user_pass("user@example.com", "password")
```

### 3. Create a Client

```python
from thematic_client_sdk import ThematicClient

client = ThematicClient(access_token)
```

To scope all requests to a specific organization:

```python
client.organization("org_name")
```

You can also configure a custom API URL and request timeout (default 30s):

```python
client = ThematicClient(access_token, api_url="https://custom-api.example.com/api", timeout=60)
```

## Usage

### Surveys

```python
# List all surveys
surveys = client.surveys.get()

# Get a specific survey
survey = client.surveys.get(survey_id=123)

# Create a survey
response = client.surveys.create("My Survey", manual_upload_allowed=True)

# Update a survey
client.surveys.update(123, {"name": "Renamed Survey"})
```

### Uploading Data

```python
# Upload data to a survey
upload_id = client.data.upload_data(survey_id, "/path/to/data.csv")

# Check upload status (poll until complete)
status = client.data.check_uploaded_data(survey_id, upload_id)
# Possible statuses: "ProcessingJobStatus.completed", "ProcessingJobStatus.errored", etc.

# Get upload logs (useful for debugging failures)
logs = client.data.log_uploaded_data(survey_id, upload_id)
```

### Downloading Results

```python
# Download processed data as CSV
client.data.download_data("output.csv", survey_id, output_format="byResponse")

# Download for a specific result
client.data.download_data("output.csv", survey_id, result_id=456)

# Download themes as JSON
client.data.download_themes("themes.json", survey_id)

# Download upload job results
client.data.download_upload_results("results.csv", survey_id, upload_id)
```

Available output formats: `"byResponse"`, `"byTheme"`, `"denormalizedResponses"`.

### Themes

```python
# Get themes for a source (current version)
themes = client.themes.get_themes(source_id)

# Get a specific version
themes = client.themes.get_themes(source_id, version="v2")

# Discover potential new themes
discovered = client.themes.discover(source_id, rql_filter="sentiment:negative", comment_limit=500)
```

Async variants are available:

```python
themes = await client.themes.get_themes_async(source_id)
```

### Visualizations

```python
# List visualizations
visualizations = client.visualizations.get(survey_id, view_id)

# Get theme volumes
counts = client.visualizations.get_counts(survey_id, view_id, vis_id, options)

# Get themes by date
trends = client.visualizations.get_themes_by_date(survey_id, view_id, vis_id, options)

# Get comments
comments = client.visualizations.get_comments(survey_id, view_id, vis_id, filter_string="theme:123")
```

Many visualization methods have async variants (e.g. `get_counts_async`, `get_themes_async`).

### Organizations

```python
# Get your organization
org = client.organizations.get()

# List all organizations
orgs = client.organizations.get_list()

# Get usage metrics
metrics = client.organizations.get_metrics(resolution="weekly", num_periods=8)
```

### Users and Roles

```python
# List users
users = client.users.get()

# Create a user
client.users.create("user@example.com", "First", "Last", roles=[1], seat_type="full")

# Manage roles
roles = client.roles.get()
client.users.add_user_to_role(user_id, role_id)
client.users.remove_user_from_role(user_id, role_id)

# Custom permissions
client.users.set_custom_permissions_for_user(user_id, policy={...})
client.users.remove_custom_permissions_for_user(user_id)
```

### Lenses

```python
# List lenses
lenses = client.lenses.get()

# Create a lens
lens = client.lenses.create("My Lens", data_sources=[...])

# Manage lens views
views = client.lens_views.get(lens_id)
view = client.lens_views.create(lens_id, "View Name")
```

### Reports and Digests

```python
# List reports
reports = client.reports.get()

# Create or update a report
client.reports.create("Report Name", version=1, is_preview_only=False, configuration={...}, update_if_exists=True)

# List digests
digests = client.digests.get()
```

### Other Resources

```python
# Analysis sources (nested survey/view/visualization structure)
sources = client.analysis_sources.get()

# Integrations
integrations = client.integrations.get_list()

# Upload jobs
jobs = client.upload_jobs.get(survey_id)

# Workflows
workflows = client.workflows.get()

# Views
views = client.views.get(survey_id)
```

## Error Handling

All API errors raise `ThematicAPIError` (a subclass of `Exception`) with the HTTP status code and response body attached:

```python
from thematic_client_sdk import ThematicAPIError

try:
    surveys = client.surveys.get()
except ThematicAPIError as e:
    print(f"API error {e.status_code}: {e}")
    print(f"Response: {e.response_text}")
```

Existing code using `except Exception` will continue to work since `ThematicAPIError` inherits from `Exception`.

## Examples

See the `example/` directory for complete scripts:

- `list_surveys.py` -- List all surveys and their visualizations
- `pull_data.py` -- Download processed data and themes
- `process_data.py` -- Upload data, poll for completion, download results

Run them with:

```bash
python example/list_surveys.py <refresh_token> <organization>
python example/pull_data.py <refresh_token> <survey_id> [output_format]
python example/process_data.py <refresh_token> <survey_id> <data_file_path>
```
