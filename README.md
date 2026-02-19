# Telavox Onboading MCP Tools 

## Get User Licenses Tool

### Overview

Retrieves available user licenses from Telavox CAPI with regional pricing based on geography and currency.

### Request Details

- Method: GET
- Endpoint: https://home.telavox.se/api/capi/v1/assortment/country-{{country_code}}/currency-{{currency_code}}/user-licenses

### Parameters

- country_code (String) | Path | Required: Yes | ISO country code (e.g., SE).
- currency_code (String) | Path | Required: Yes | Currency code (e.g., SEK).

## Purchase User Licenses Tool


### Overview

Executes a purchase of specific user licenses through the Telavox CAPI. It allows for specifying quantity and optional invoice placement within a regional context.

### Request Details

- Method: POST
- Endpoint: https://home.telavox.se/api/capi/v1/products/user-licenses/country-{{country_code}}/currency-{{currency_code}}/{{assortment_key}}

### Parameters

- country_code (String) | Path | Required: Yes | ISO country code (e.g., SE).
- currency_code (String) | Path | Required: Yes | Currency code (e.g., SEK).
- assortment_key (String) | Path | Required: Yes | The unique identifier for the license type.
- invoice_place (String) | Query | Required: No | Specific billing location identifier.
- quantity (Number) | Query | Required: No | Number of licenses to purchase (Defaults to 1).

## List Users Tool

### Overview

Retrieves a list of user extensions from the Telavox CAPI. The request can be filtered by a specific phone number or narrowed down by a specific invoice placement.

### Request Details

- Method: GET
- Endpoint: https://home.telavox.se/api/capi/v1/extensions/users

### Parameters

- number (String) | Query | Required: No | Filter the list by a specific phone number.
- invoice_place (String) | Query | Required: No | Filter the list by a specific billing location identifier.

## Create User Tool

### Overview

Creates a new user extension within the Telavox system. This tool allows for configuration of the user's region, billing location, email, and configuration template, with an option to send a confirmation email upon creation.

### Request Details

- Method: POST
- Endpoint: https://home.telavox.se/api/capi/v1/extensions/users

### Parameters

- country_code (String) | Query | Required: Yes | ISO country code used to set the user's region (e.g., SE).
- invoice_place (String) | Query | Required: No | The specific billing location identifier for the new user.
- email (String) | Query | Required: No | The email address associated with the new user extension.
- template (String) | Query | Required: No | The identifier for a predefined configuration template to apply.
- confirmation_email (Boolean) | Query | Required: No | Whether to send a confirmation email to the user (Defaults to false).

## Update User Tool

### Overview

Updates an existing user extension's profile and configuration in the Telavox CAPI. This tool allows for modifying user details such as name, assigned phone numbers, billing location, and license types.

### Request Details

- Method: PUT
- Endpoint: https://home.telavox.se/api/capi/v1/extensions/users/{{user}}

### Parameters

- user (String) | Path | Required: Yes | The unique identifier or key of the user extension to update.
- body (Object) | Body | Required: Yes | A JSON object containing the user fields to update (e.g., name, fixedNumber, mobileNumber, invoicePlace, licenseType).

## List Invoice Places Tool

### Overview

Retrieves a list of valid invoice places (billing locations) for a specific country from the Telavox CAPI. This is useful for identifying correct billing identifiers required when creating or updating users.

### Request Details

- Method: GET
- Endpoint: https://home.telavox.se/api/capi/v1/invoice-places/country-{{country_code}}

### Parameters

- country_code (String) | Path | Required: Yes | The ISO country code (e.g., SE) to filter the billing locations.

## List Templates Tool

### Overview

Retrieves a list of available configuration templates from the Telavox CAPI. These templates are used to apply predefined settings and configurations when creating or managing user extensions.

### Request Details

- Method: GET
- Endpoint: https://home.telavox.se/api/capi/v1/templates

### Parameters

- No parameters required.

## List Available Reserved Phone Numbers Tool

### Overview

Retrieves a paginated list of available reserved phone numbers from the Telavox CAPI for a specific country. This allows users to browse and select from the inventory of numbers currently held by the organization.

### Request Details

- Method: GET
- Endpoint: https://home.telavox.se/api/capi/v1/reserved-phone-numbers/available

### Parameters

- country_code (String) | Query | Required: Yes | ISO country code used to filter the numbers (e.g., SE).
- page_size (Number) | Query | Required: No | The number of results to return per page (Defaults to 50).
- page_number (Number) | Query | Required: No | The specific page index to retrieve (Defaults to 0).

## Purchase Phone Number Tool

### Overview

Purchases one or multiple phone numbers from the reserved inventory and assigns them to the organization's account. This tool requires a list of number objects and an optional billing location.

### Request Details

- Method: POST
- Endpoint: https://home.telavox.se/api/capi/v1/reserved-phone-numbers

### Parameters

- body (Array) | Body | Required: Yes | An array of objects containing number details (e.g., e164Number, country, usages, key).
- invoice_place (String) | Query | Required: No | The specific billing location identifier (passed as `invoiceplace`) to associate with the purchase.

## Port Phone Number Tool

### Overview

Initiates the porting process to transfer an existing phone number from another operator to Telavox. This tool handles the submission of porting requests, including preferred dates and organizational authorization details.

### Request Details

- Method: POST
- Endpoint: https://home.telavox.se/api/capi/v1/portings

### Parameters

- phone_number (String) | Query | Required: Yes | The phone number to be ported in E.164 format (passed as `startE164Number`).
- body (Object) | Body | Required: Yes | A JSON object containing porting details such as `preferredPortingDate`, `orgNumber`, and the requested `state`.

### Notes

- The `phone_number` value should be a full E.164 number (for example `+46739983281`). The client will URL-encode the `+` automatically when sending `startE164Number` as a query parameter.

## List Groups Tool

### Overview

Retrieves a list of all groups (such as queues or ring groups) configured within the Telavox system. This is useful for identifying group keys for routing or management purposes.

### Request Details

- Method: GET
- Endpoint: https://home.telavox.se/api/capi/v1/groups

### Parameters

- No parameters required.

## Update Group Members Tool

### Overview

Updates the membership list for a specific group (such as a queue or ring group) in the Telavox CAPI. This tool effectively sets the members of the specified group by replacing or adding the provided extension keys.

### Request Details

- Method: PUT
- Endpoint: https://home.telavox.se/api/capi/v1/groups/{{group_key}}/members

### Parameters

- group_key (String) | Path | Required: Yes | The unique identifier for the group to be updated.
- member_keys (String) | Query | Required: Yes | A comma-separated list of extension keys to be assigned as members (passed as `memberKeys`).

## Get Available Add-ons Tool

### Overview

Retrieves a list of compatible and available add-on products for a specific user extension from the Telavox CAPI. This tool is used to identify which additional services or features can be purchased or assigned to a particular user.

### Request Details

- Method: GET
- Endpoint: https://home.telavox.se/api/capi/v1/assortment/addons/{{user}}

### Parameters

- user (String) | Path | Required: Yes | The unique identifier or extension key (e.g., extension-7422411) of the user.

## Purchase Add-on Tool

### Overview

Executes the purchase and assignment of a specific add-on product to a user extension. This tool links a chosen assortment item (identified via the "Get Available Add-ons Tool") directly to a user's account.

### Request Details

- Method: POST
- Endpoint: https://home.telavox.se/api/capi/v1/products/addons/{{user}}/{{assortment_item}}

### Parameters

- user (String) | Path | Required: Yes | The unique identifier or extension key of the user.
- assortment_item (String) | Path | Required: Yes | The unique key of the add-on product to be purchased.

## List Queues Tool

### Overview

Retrieves a comprehensive list of all call queues configured within the Telavox system. This tool provides the necessary identifiers for queue management and reporting.

### Request Details

- Method: GET
- Endpoint: https://home.telavox.se/api/capi/v1/queues

### Parameters

- No parameters required.

## Add Queue Members Tool

### Overview

Assigns new members to a specific PBX call queue. This tool takes a target queue extension and an array of member objects to define who should be answering calls for that specific queue.

### Request Details

- Method: POST
- Endpoint: https://home.telavox.se/api/capi/v1/extensions/pbx/queues/{{extension}}/members

### Parameters

- extension (String) | Path | Required: Yes | The extension identifier of the target PBX queue.
- body (Array) | Body | Required: Yes | An array of member objects defining the extensions to be added to the queue.

## Get Colleague Tool

### Overview

Retrieves detailed contact and profile information for a specific colleague within the Telavox system using their user identifier.

### Request Details

- Method: GET
- Endpoint: https://home.telavox.se/api/capi/v1/contacts/colleagues/{{user}}

### Parameters

- user (String) | Path | Required: Yes | The unique identifier or key of the colleague/user to retrieve.
