import sys
import os
import logging
import base64
import json
from urllib.parse import urljoin
from core.io import HttpRequests

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../'))


class JamfAdapter(HttpRequests.HttpExecutor):
    """
    Adapter for interacting with the Jamf API.
    Handles authentication and common operations with dynamic endpoint support.
    """

    api_endpoints = {
        "accounts": "JSSResource/accounts",
        "activation_code": "JSSResource/activationcode",
        "advanced_computer_searches": "JSSResource/advancedcomputersearches",
        "advanced_mobile_device_searches": "JSSResource/advancedmobiledevicesearches",
        "advanced_user_searches": "JSSResource/advancedusersearches",
        "allowed_file_extensions": "JSSResource/allowedfileextensions",
        "buildings": "JSSResource/buildings",
        "byo_profiles": "JSSResource/byoprofiles",
        "categories": "JSSResource/categories",
        "classes": "JSSResource/classes",
        "command_flush": "JSSResource/commandflush",
        "computer_applications": "JSSResource/computerapplications",
        "computer_application_usage": "JSSResource/computerapplicationusage",
        "computer_checkin": "JSSResource/computercheckin",
        "computer_commands": "JSSResource/computercommands",
        "computer_extension_attributes": "JSSResource/computerextensionattributes",
        "computer_groups": "JSSResource/computergroups",
        "computer_hardware_software_reports": "JSSResource/computerhardwaresoftwarereports",
        "computer_history": "JSSResource/computerhistory",
        "computer_inventory_collection": "JSSResource/computerinventorycollection",
        "computer_invitations": "JSSResource/computerinvitations",
        "computer_management": "JSSResource/computermanagement",
        "computer_reports": "JSSResource/computerreports",
        "computers": "JSSResource/computers",
        "departments": "JSSResource/departments",
        "directory_bindings": "JSSResource/directorybindings",
        "disk_encryption_configurations": "JSSResource/diskencryptionconfigurations",
        "distribution_points": "JSSResource/distributionpoints",
        "dock_items": "JSSResource/dockitems",
        "ebooks": "JSSResource/ebooks",
        "file_uploads": "JSSResource/fileuploads",
        "gsx_connection": "JSSResource/gsxconnection",
        "healthcare_listener": "JSSResource/healthcarelistener",
        "healthcare_listener_rule": "JSSResource/healthcarelistenerrule",
        "ibeacons": "JSSResource/ibeacons",
        "infrastructure_manager": "JSSResource/infrastructuremanager",
        "jss_user": "JSSResource/jssuser",
        "json_web_token_configurations": "JSSResource/jsonwebtokenconfigurations",
        "ldap_servers": "JSSResource/ldapservers",
        "licensed_software": "JSSResource/licensedsoftware",
        "log_flush": "JSSResource/logflush",
        "mac_applications": "JSSResource/macapplications",
        "mobile_device_applications": "JSSResource/mobiledeviceapplications",
        "mobile_device_commands": "JSSResource/mobiledevicecommands",
        "mobile_device_configuration_profiles": "JSSResource/mobiledeviceconfigurationprofiles",
        "mobile_device_enrollment_profiles": "JSSResource/mobiledeviceenrollmentprofiles",
        "mobile_device_extension_attributes": "JSSResource/mobiledeviceextensionattributes",
        "mobile_device_groups": "JSSResource/mobiledevicegroups",
        "mobile_device_history": "JSSResource/mobiledevicehistory",
        "mobile_device_invitations": "JSSResource/mobiledeviceinvitations",
        "mobile_device_provisioning_profiles": "JSSResource/mobiledeviceprovisioningprofiles",
        "mobile_devices": "JSSResource/mobiledevices",
        "network_segments": "JSSResource/networksegments",
        "osx_configuration_profiles": "JSSResource/osxconfigurationprofiles",
        "packages": "JSSResource/packages",
        "patch_available_titles": "JSSResource/patchavailabletitles",
        "patches": "JSSResource/patches",
        "patch_external_sources": "JSSResource/patchexternalsources",
        "patch_internal_sources": "JSSResource/patchinternalsources",
        "patch_policies": "JSSResource/patchpolicies",
        "patch_reports": "JSSResource/patchreports",
        "patch_software_titles": "JSSResource/patchsoftwaretitles",
        "peripherals": "JSSResource/peripherals",
        "peripheral_types": "JSSResource/peripheraltypes",
        "policies": "JSSResource/policies",
        "printers": "JSSResource/printers",
        "removable_mac_addresses": "JSSResource/removablemacaddresses",
        "restricted_software": "JSSResource/restrictedsoftware",
        "saved_searches": "JSSResource/savedsearches",
        "scripts": "JSSResource/scripts",
        "sites": "JSSResource/sites",
        "smtp_server": "JSSResource/smtpserver",
        "software_update_servers": "JSSResource/softwareupdateservers",
        "user_extension_attributes": "JSSResource/userextensionattributes",
        "user_groups": "JSSResource/usergroups",
        "users": "JSSResource/users",
        "vpp_accounts": "JSSResource/vppaccounts",
        "vpp_assignments": "JSSResource/vppassignments",
        "vpp_invitations": "JSSResource/vppinvitations",
        "webhooks": "JSSResource/webhooks",
        "activation_code": "api/v1/activation-code",
        "advanced_mobile_device_searches": "api/v1/advanced-mobile-device-searches",
        "advanced_user_content_searches": "api/v1/advanced-user-content-searches",
        "api_authentication": "api/v1/api-authentication",
        "api_integrations": "api/v1/api-integrations",
        "api_role_privileges": "api/v1/api-role-privileges",
        "api_roles": "api/v1/api-roles",
        "app_request_preview": "api/v1/app-request-preview",
        "app_store_country_codes_preview": "api/v1/app-store-country-codes-preview",
        "branding": "api/v1/branding",
        "buildings": "api/v1/buildings",
        "cache_settings": "api/v1/cache-settings",
        "categories": "api/v1/categories",
        "certificate_authority": "api/v1/certificate-authority",
        "classic_ldap": "api/v1/classic-ldap",
        "client_check_in": "api/v1/client-check-in",
        "cloud_azure": "api/v1/cloud-azure",
        "cloud_distribution_point": "api/v1/cloud-distribution-point",
        "cloud_idp": "api/v1/cloud-idp",
        "cloud_information": "api/v1/cloud-information",
        "cloud_ldap": "api/v1/cloud-ldap",
        "computer_extension_attributes": "api/v1/computer-extension-attributes",
        "computer_groups": "api/v1/computer-groups",
        "computer_inventory": "api/v1/computer-inventory",
        "computer_inventory_collection_settings": "api/v1/computer-inventory-collection-settings",
        "computer_prestages": "api/v1/computer-prestages",
        "computers_preview": "api/v1/computers-preview",
        "conditional_access": "api/v1/conditional-access",
        "csa": "api/v1/csa",
        "dashboard": "api/v1/dashboard",
        "declarative_device_management": "api/v1/declarative-device-management",
        "departments": "api/v1/departments",
        "device_communication_settings": "api/v1/device-communication-settings",
        "device_enrollments": "api/v1/device-enrollments",
        "device_enrollments_devices": "api/v1/device-enrollments-devices",
        "dock_items": "api/v1/dock-items",
        "dss_declarations": "api/v1/dss-declarations",
        "ebooks": "api/v1/ebooks",
        "engage": "api/v1/engage",
        "enrollment": "api/v1/enrollment",
        "enrollment_customization": "api/v1/enrollment-customization",
        "enrollment_customization_preview": "api/v1/enrollment-customization-preview",
        "gsx_connection": "api/v1/gsx-connection",
        "health_check": "api/v1/health-check",
        "icon": "api/v1/icon",
        "inventory_information": "api/v1/inventory-information",
        "inventory_preload": "api/v1/inventory-preload",
        "jamf_connect": "api/v1/jamf-connect",
        "jamf_content_distribution_server": "api/v1/jamf-content-distribution-server",
        "jamf_management_framework": "api/v1/jamf-management-framework",
        "jamf_package": "api/v1/jamf-package",
        "jamf_pro_account_preferences": "api/v1/jamf-pro-account-preferences",
        "jamf_pro_information": "api/v1/jamf-pro-information",
        "jamf_pro_initialization": "api/v1/jamf-pro-initialization",
        "jamf_pro_notifications": "api/v1/jamf-pro-notifications",
        "jamf_pro_notifications_preview": "api/v1/jamf-pro-notifications-preview",
        "jamf_pro_server_url_preview": "api/v1/jamf-pro-server-url-preview",
        "jamf_pro_user_account_settings": "api/v1/jamf-pro-user-account-settings",
        "jamf_pro_user_account_settings_preview": "api/v1/jamf-pro-user-account-settings-preview",
        "jamf_pro_version": "api/v1/jamf-pro-version",
        "jamf_protect": "api/v1/jamf-protect",
        "jamf_remote_assist": "api/v1/jamf-remote-assist",
        "ldap": "api/v1/ldap",
        "local_admin_password": "api/v1/local-admin-password",
        "locales_preview": "api/v1/locales-preview",
        "login_customization": "api/v1/login-customization",
        "macos_managed_software_updates": "api/v1/macos-managed-software-updates",
        "managed_software_updates": "api/v1/managed-software-updates",
        "mdm": "api/v1/mdm",
        "mobile_device_apps": "api/v1/mobile-device-apps",
        "mobile_device_enrollment_profile": "api/v1/mobile-device-enrollment-profile",
        "mobile_device_extension_attributes_preview": "api/v1/mobile-device-extension-attributes-preview",
        "mobile_device_groups": "api/v1/mobile-device-groups",
        "mobile_device_prestages": "api/v1/mobile-device-prestages",
        "mobile_devices": "api/v1/mobile-devices",
        "oidc": "api/v1/oidc",
        "onboarding": "api/v1/onboarding",
        "packages": "api/v1/packages",
        "parent_app_preview": "api/v1/parent-app-preview",
        "patch_management": "api/v1/patch-management",
        "patch_policies": "api/v1/patch-policies",
        "patch_policy_logs": "api/v1/patch-policy-logs",
        "patch_software_title_configurations": "api/v1/patch-software-title-configurations",
        "policies_preview": "api/v1/policies-preview",
        "re_enrollment_preview": "api/v1/re-enrollment-preview",
        "remote_administration": "api/v1/remote-administration",
        "return_to_service": "api/v1/return-to-service",
        "scheduler": "api/v1/scheduler",
        "scripts": "api/v1/scripts",
        "self_service": "api/v1/self-service",
        "self_service_branding_ios": "api/v1/self-service-branding-ios",
        "self_service_branding_macos": "api/v1/self-service-branding-macos",
        "self_service_branding_preview": "api/v1/self-service-branding-preview",
        "sites": "api/v1/sites",
        "sites_preview": "api/v1/sites-preview",
        "slasa": "api/v1/slasa",
        "smart_computer_groups_preview": "api/v1/smart-computer-groups-preview",
        "smart_mobile_device_groups_preview": "api/v1/smart-mobile-device-groups-preview",
        "smart_user_groups_preview": "api/v1/smart-user-groups-preview",
        "smtp_server": "api/v1/smtp-server",
        "sso_certificate": "api/v1/sso-certificate",
        "sso_certificate_preview": "api/v1/sso-certificate-preview",
        "sso_failover": "api/v1/sso-failover",
        "sso_oauth_session_tokens": "api/v1/sso-oauth-session-tokens",
        "sso_settings": "api/v1/sso-settings",
        "startup_status": "api/v1/startup-status",
        "static_user_groups_preview": "api/v1/static-user-groups-preview",
        "supervision_identities_preview": "api/v1/supervision-identities-preview",
        "teacher_app": "api/v1/teacher-app",
        "team_viewer_remote_administration": "api/v1/team-viewer-remote-administration",
        "time_zones_preview": "api/v1/time-zones-preview",
        "tomcat_settings_preview": "api/v1/tomcat-settings-preview",
        "user": "api/v1/user",
        "user_session_preview": "api/v1/user-session-preview",
        "venafi_preview": "api/v1/venafi-preview",
        "volume_purchasing_locations": "api/v1/volume-purchasing-locations",
        "volume_purchasing_subscriptions": "api/v1/volume-purchasing-subscriptions",
    }


    def __init__(self, username, password, base_url, verify_ssl=True):
        """
        Initialize the Jamf API adapter.

        Args:
            username (str): Username for Basic authentication.
            password (str): Password for Basic authentication.
            base_url (str): Base URL for Jamf API.
            verify_ssl (bool): Whether to verify SSL certificates. Default is True.
        """
        self.username = username
        self.password = password
        self.token = None
        self.base_url = base_url.rstrip("/")  # Ensure no trailing slash
        super().__init__(base_url, verify_ssl)

    def get_endpoint(self, object_type, object_id=None):
        """
        Retrieve the endpoint for the given object type and format it dynamically.

        Args:
            object_type (str): The name of the object type.
            object_id (str, optional): ID of the specific object.

        Returns:
            str: The constructed endpoint URL.
        """
        base_endpoint = self.api_endpoints.get(object_type)
        if not base_endpoint:
            raise ValueError(f"Invalid object type '{object_type}'. No endpoint found.")

        if object_id:
            # Append `/id/{id}` or `/{id}` for specific objects
            if "v1" in base_endpoint:  # For API v1
                base_endpoint = f"{base_endpoint}/{object_id}"
            else:
                base_endpoint = f"{base_endpoint}/id/{object_id}"

        # Ensure proper URL construction
        return urljoin(self.base_url + "/", base_endpoint)

    def _get_headers(self, token=None):
        """
        Generate standard headers for requests, including token if available.

        Args:
            token (str, optional): Token for Bearer authentication.

        Returns:
            dict: Headers for the request.
        """
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if token or self.token:
            headers["Authorization"] = f"Bearer {token or self.token}"
        return headers

    def _get_basic_auth(self):
        """
        Generate a Base64-encoded Basic authentication string.

        Returns:
            str: Base64-encoded username:password.
        """
        if not self.username or not self.password:
            raise ValueError("Both username and password must be provided for Basic authentication.")
        return base64.b64encode(f"{self.username}:{self.password}".encode()).decode()

    def get_token(self):
        """
        Retrieve a Bearer token for authentication.

        Returns:
            str: The Bearer token.

        Raises:
            ValueError: If the token cannot be retrieved.
        """
        endpoint = self.get_endpoint("oauth")
        headers = {"Authorization": f"Basic {self._get_basic_auth()}"}

        try:
            response = self.request(endpoint, method="POST", headers=headers)
            self.token = response.json().get("token")
            if not self.token:
                raise ValueError("Failed to retrieve token.")
            return self.token
        except Exception as e:
            logging.error(f"Failed to retrieve token: {e}")
            raise ValueError("Failed to retrieve token.") from e

    def get_oauth_token(self, client_id, client_secret, grant_type="client_credentials"):
        """
        Retrieve an OAuth token using client credentials.

        Args:
            client_id (str): OAuth client ID.
            client_secret (str): OAuth client secret.
            grant_type (str): OAuth grant type. Default is "client_credentials".

        Returns:
            str: OAuth access token.
        """
        endpoint = self.get_endpoint("oauth")
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"client_id": client_id, "client_secret": client_secret, "grant_type": grant_type}

        try:
            response = self.request(endpoint, method="POST", headers=headers, data=data)
            return response.json().get("access_token")
        except Exception as e:
            logging.error(f"Failed to retrieve OAuth token: {e}")
            raise ValueError("Failed to retrieve OAuth token.") from e

    def invalidate_token(self):
        """
        Invalidate the current Bearer token.

        Returns:
            dict: Response from the server.
        """
        endpoint = self.get_endpoint("invalidate")
        self._ensure_token()

        try:
            response = self.request(endpoint, method="POST", headers=self._get_headers())
            self.token = None  # Reset the token
            return response.json()
        except Exception as e:
            logging.error(f"Failed to invalidate token: {e}")
            raise ValueError("Failed to invalidate token.") from e

    def get_object(self, object_type, object_id=None, auth_method="Bearer", method="GET", payload=None, params=None):
        """
        Retrieve or interact with an object using a specified HTTP method.

        Args:
            object_type (str): The object type to fetch.
            object_id (str, optional): The ID of the object to fetch.
            auth_method (str): Authentication method, either "Basic", "Bearer", or "OAuth".
            method (str): HTTP method to use (e.g., "GET", "POST", "PUT", "DELETE").
            payload (dict, optional): JSON payload for the request.
            params (dict, optional): Query parameters for the request.

        Returns:
            dict: The response JSON containing the object(s).
        """
        endpoint = self.get_endpoint(object_type, object_id=object_id)

        # Determine headers based on auth_method
        if auth_method == "Bearer":
            self._ensure_token()
            headers = self._get_headers()
        elif auth_method == "Basic":
            headers = {"Authorization": f"Basic {self._get_basic_auth()}"}
        elif auth_method == "OAuth":
            headers = self._get_headers()
        else:
            raise ValueError("Invalid authentication method. Use 'Basic', 'Bearer', or 'OAuth'.")

        # Enforce JSON response in headers
        headers["Accept"] = "application/json"

        # Prepare request arguments
        request_args = {"method": method, "headers": headers}
        if method == "GET" and params:
            request_args["params"] = params
        elif method in {"POST", "PUT", "PATCH", "DELETE"} and payload:
            request_args["data"] = json.dumps(payload)

        # Debugging the request
        logging.debug(f"Request: {method} {endpoint}")
        logging.debug(f"Headers: {headers}")
        logging.debug(f"Params: {params}, Payload: {payload}")

        try:
            response = self.request(endpoint, **request_args)

            # Check if JSON is returned
            if "application/json" in response.headers.get("Content-Type", ""):
                return response.json()

            # Fallback to raw response for non-JSON
            logging.warning(f"Non-JSON response received for '{object_type}': {response.text}")
            return response.text

        except Exception as e:
            logging.error(f"Failed to interact with '{object_type}' (Method: {method}, Endpoint: {endpoint}): {e}")
            raise ValueError(f"Failed to interact with '{object_type}'.") from e
