def save_docs_data_per_stage(claim_id,key_list_chain,data_list_chain,additional_data={}):
    # Global logging control variable
    DEBUG_LOGGING = True

    def debug_log(message):
        if DEBUG_LOGGING:
            LOG.info(message)

    try:
        # Log the input parameters with more context
        debug_log(f"Method: save_docs_data_per_stage")
        debug_log(f"Claim ID: {claim_id}")
        debug_log(f"Key list chain length: {len(key_list_chain)}")
        debug_log(f"Data list chain length: {len(data_list_chain)}")
        debug_log(f"Key list chain: {key_list_chain}")
        debug_log(f"Data list chain: {data_list_chain}")
        debug_log(f"Additional data keys: {list(additional_data.keys()) if additional_data else 'No additional data'}")

        try:
            # Log S3 data retrieval attempt with full path
            s3_path = f"jsons/{claim_id}/"
            debug_log(f"Attempting to retrieve evaluation_metrics.json from S3 path: {s3_path}")
            s3_json = get_data_from_s3(s3_path, "evaluation_metrics.json")
            debug_log(f"Successfully retrieved evaluation_metrics.json. Existing data keys: {list(s3_json.keys()) if s3_json else 'Empty'}")
        except Exception as e:
            # Log the exception during S3 data retrieval with more details
            s3_json = {}
            LOG.info(f"Error retrieving evaluation_metrics.json from S3: {str(e)}")
            debug_log(f"Detailed retrieval error: {traceback.format_exc()}")
            debug_log(f"Defaulting to empty JSON due to retrieval error")
 
        if not s3_json:
            # Log JSON initialization with more context
            debug_log("No existing JSON found. Initializing empty evaluation_metrics JSON structure")
            s3_json = {'extracted':{},'qc_modified':{},'qc_verified':{},'final_sent':{}}

        debug_log(f"Initial s3_json structure: {s3_json}")
        
        # Log JSON update process with more details
        debug_log("Starting JSON update process")
        for i, j in zip(key_list_chain, data_list_chain):
            debug_log(f"Updating nested key: {i}")
            debug_log(f"Update value type: {type(j)}")
            s3_json = update_nested_json(s3_json, i, j)
        debug_log("Completed JSON updates")
        debug_log(f"Updated s3_json structure: {s3_json}")

        # Log directory creation with full path details
        local_dir = os.path.join(APP.config["JSON_DIR"], claim_id)
        debug_log(f"Ensuring directory exists: {local_dir}")
        os.makedirs(local_dir, exist_ok=True)

        # Log file writing process with full path and additional context
        local_file_path = os.path.join(local_dir, "evaluation_metrics.json")
        debug_log(f"Preparing to write JSON to local file: {local_file_path}")
        debug_log(f"File write JSON size: {len(json.dumps(s3_json))} bytes")
        
        with open(local_file_path, "w") as file:
            json.dump(s3_json, file)
        debug_log(f"Successfully wrote JSON
