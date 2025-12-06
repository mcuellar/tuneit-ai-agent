# Example Job Descriptions

This directory contains sample job descriptions that you can use to test the TuneIt AI Agent.

## Available Examples

### 1. Senior Python Developer (`senior_python_developer.txt`)
A comprehensive job description for a senior Python developer position at a tech company. This example includes:
- Detailed requirements and qualifications
- Responsibilities and nice-to-have skills
- Company benefits and culture information

### 2. AI/ML Engineer (`ai_ml_engineer.txt`)
A job description for an AI/ML Engineer position focusing on machine learning infrastructure. This example includes:
- Machine learning specific requirements
- MLOps and infrastructure experience
- Research and experimentation background

## How to Use These Examples

### Option 1: Copy to Watch Directory

While the agent is running, copy any example to the watch directory:

```bash
# Copy an example file
cp examples/senior_python_developer.txt job_descriptions/

# The agent will automatically detect and process it
```

### Option 2: Create Your Own

Use these examples as templates to create your own job descriptions:

```bash
# Copy and edit
cp examples/senior_python_developer.txt job_descriptions/my_job.txt
nano job_descriptions/my_job.txt
```

### Option 3: Test Multiple at Once

Test batch processing by copying multiple examples:

```bash
# Copy all examples
cp examples/*.txt job_descriptions/

# The agent will process each one sequentially
```

## Testing Workflow

To test the complete workflow:

1. **Start the agent:**
   ```bash
   python run.py
   ```

2. **Copy an example:**
   ```bash
   cp examples/senior_python_developer.txt job_descriptions/test_job_1.txt
   ```

3. **Watch the logs:**
   - The agent should detect the new file
   - Process it through the workflow
   - Call the MCP server tools
   - Log the results

4. **Check the output:**
   - Look for success/error messages in the console
   - Check the log file: `tuneit_agent.log`
   - Verify outputs saved by the MCP server

## Creating Your Own Examples

When creating your own job description files:

1. **Use allowed extensions:** `.txt`, `.md`, or `.pdf` (configurable in `.env`)
2. **Include key information:**
   - Position title
   - Company name
   - Requirements and qualifications
   - Responsibilities
   - Any other relevant details

3. **Format:** Plain text works best, but markdown is also supported

## Expected MCP Server Behavior

When processing these examples, the MCP server should:

1. **format_job_description**: Extract and structure the key information
2. **generate_tailored_resume**: Create a resume highlighting relevant experience
3. **save_tailored_resume**: Save the generated resume to a file
4. **save_job_description**: Save the formatted job description

## Tips

- Start with simple examples to verify basic functionality
- Use descriptive filenames (e.g., `company_position_date.txt`)
- Avoid special characters in filenames
- Keep examples up-to-date with current job market trends
- Add your own examples based on real job postings you're interested in
