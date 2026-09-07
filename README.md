# QuickBooks Accounts Payable Agent 
This repository contains the baseline for a proposed capstone project to build an accounts payable agent for a small business.  Note: AI assistance was used extensively for the creation of the Python file and for some inspiration regarding the structure of the JSON file.  The JSON File was largely produced by working with the n8n GUI.  AI was also used to research documentation for Markup language to format the instructions below

## How to Reproduce the Results

Follow these steps to set up the workflow locally:

1. **Set up n8n**: Create an [n8n trial account](https://n8n.io/).
2. **Configure QuickBooks**: 
   - Follow the instructions in the [first 3 minutes of this YouTube video](https://www.youtube.com/watch?v=mprQ4CY3yn0) to create a QuickBooks developer account and link it to n8n.
   - *Note: you do not need to watch step 2 or later of the video – this gentleman just did an excellent job within step 1 explaining what you need to do.  I am not normally one to refer you to someone's YouTube video but his explanation is so much more succinct than what I can type here*
3. **Import Workflow**:
   - Import the `.json` file found in this repository into your n8n instance.
   - **Important**: You may need to manually copy the contents of the provided Python file into the `Check for Duplicate` node.
4. **Test the System**:  Test the system with a curl request to the appropriate site.  Here is the command used for the demo system but your domain will be different since you have set up your own n8n account: :
   ```bash
   curl -X POST https://your-n8n-instance.cloud/webhook/invoice-upload \
     -H "Content-Type: application/pdf" \
     --data-binary @path/from/pwd/to/test-invoice.pdf
   ```

5. **Verify:** Look into QuickBooks accounts payable, you should now see the invoice added if everything is functioning.
