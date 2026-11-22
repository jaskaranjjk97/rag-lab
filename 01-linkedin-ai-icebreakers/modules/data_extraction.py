import time 
import json
import requests
from typing import Any,Optional
import logging
import config

from modules.data_preprocessing import normalize_harvestapi_profile

logger=logging.getLogger(__name__)

def extract_linkedin_profile(
        linkedin_profile_url:str,
        mock: bool = False,
        api_key: Optional[str] = None
)-> dict[str, Any]:

    start_time = time.time()
    if mock:
        logger.info("Loading local mock profile data...")

        with open(config.MOCK_DATA_PATH, "r", encoding="utf-8") as file:
            profile = json.load(file)

        return profile
    else:
        token = api_key or config.APIFY_API_TOKEN
        if not token:
            raise ValueError("Apify API key is required when mock is set to False.")

        url=config.APIFY_API_ENDPOINT
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
        "profileScraperMode": "Profile details no email ($4 per 1k)",
        "queries": [linkedin_profile_url]
}

        logger.info("Sending profile extraction request to HarvestAPI...")
        try:
            response=requests.post(url=url,headers=headers,json=payload,timeout=310)
            response.raise_for_status()
            data=response.json()

        except requests.RequestException as e:
            logger.exception("Profile extraction API request failed.")
            raise RuntimeError("Could not retrieve LinkedIn profile.") from e

        except ValueError as e:
            logger.exception("Invalid JSON received from extraction API.")
            raise ValueError("The extraction API returned invalid JSON.") from e

        # Apify returns a list containing the extraction result.
        if isinstance(data, list):
            if not data:
                raise ValueError("No profile data was returned.")

            raw_profile = data[0]

        elif isinstance(data,dict):
            raw_profile=data

        else:
            raise ValueError("Unexpected HarvestAPI response format.")

        if not isinstance(raw_profile, dict) or not raw_profile:
            raise ValueError("No valid profile information was returned.")

        # Convert HarvestAPI fields into our application's standard schema.
        profile = normalize_harvestapi_profile(raw_profile)

        if not profile.get("full_name"):
            raise ValueError("The extracted profile does not contain a valid name.")

        elapsed_time = time.time() - start_time

        logger.info(
            f"Successfully extracted profile for "
            f"{profile.get('full_name')} "
            f"in {elapsed_time:.2f} seconds."
        )

        return profile
