# Webscraping Scripts - Operational Runbook

## Table of Contents

1. [Introduction](#introduction)
2. [Code base](#code-base)
3. [List of servers and scripts](#list-of-servers-and-scripts)
4. [General Operations Steps](#general-operations-steps)
   - [Logging on to the server](#logging-on-to-the-server)
   - [Working with cron schedules](#working-with-cron-schedules)
   - [Running a Python Script](#running-a-python-script)
5. [Known Issues](#known-issues)
6. [Common Python Modules](#common-python-modules)
7. [Details of Scripts](#details-of-scripts)

---

## [Introduction](#introduction)

The key purpose of this document is to enable the dev team to execute, monitor and manage web scraping scripts.

## [Code base](#code-base)

The latest version of the code is available on git: https://github.com/daviefogarty/MOAS-scrapers/tree/master

## [List of servers and scripts](#list-of-servers-and-scripts)

| **Server**      | **Script name**                   |
| --------------- | --------------------------------- |
| 207.244.239.107 | ads_library_lf_updated            |
|                 | save_ads_new_method               |
|                 |                                   |
| 207.244.246.21  | redit_cron                        |
|                 | vstat_scrape                      |
|                 | trustpilot_review_updated_run     |
|                 | shopify_store_reviews_updated_run |
|                 | save_brand_master                 |
|                 | shopify_reviews_save_brand        |
|                 | freightos_new_run2                |
|                 | shopify_checker2                  |
|                 | get_insta_urls                    |
|                 |                                   |
| 207.244.237.135 | redit_cron                        |
|                 | vstat_scrape                      |
|                 | trustpilot_review_updated_run     |
|                 | shopify_store_reviews_updated_run |
|                 | shopify_theme_updated_run         |
|                 | similarweb_new_run                |
|                 |                                   |
| 209.145.59.158  | shopify_store_reviews_updated_run |
|                 | redit_cron                        |
|                 | similarweb_new_run                |
|                 |                                   |
| 207.244.238.128 | trustpilot_review_updated_run     |
|                 | domain_search                     |
|                 | vstat_scrape_run                  |
|                 | dropship_update                   |
|                 |                                   |
| 209.145.48.140  | shopify_products_optimized_run    |
|                 | shopify_best_seller_run.py        |
| 95.111.230.152  | similarweb_new_run                |

## [General Operations Steps](#general-operations-steps)

### [Logging on to the server](#logging-on-to-the-server)

Follow the below steps to log on the server.

1. Lookup the IP address from the above table that you want to connect to. (FYI - currently servers are hosted via Contabo. If you need to manage the servers, go to https://my.contabo.com/account/login and login using credentials available in 1password "Engineering" vault. )
2. Launch a SSH tool like putty for CLI based interface or WinSCP for GUI based expereince. Create a new connection for the IP address of the desired server. The username/password is available om 1password "Servers" vault.
3. The port# for establishing connection is 22. However, in future if it needs to be changed, it can be done via contabo login console.
4. If using WinSCP, the file protocol is SFTP. It is selected by default but in case, one has to type in the file protocol, use SFTP.

### [Working with cron schedules](#working-with-cron-schedules)

Scripts are scheduled to run via crontab utility.

- To view the scheduled task, type **crontab -l** in the terminal.
- To add/edit the schedules, type **crontab -e** . '-e' will open the default editor to edit the file. Usally the editors are 'vi' or 'nano'.
- The schedules use the system time to trigger a task. In order to check the system time type **date** in the terminal to see the current time and timezone of the server.
- Schedule the task accordingly. Alternatively you can also set the timezone of you task explicitly by typing **"TZ=[your desired timezone] e.g. America/New_York"**

### [Running a Python Script](#running-a-python-script)

Triggering a python script is very straing forward.

- Type **python3 [space] [path of the file]** e.g. python3 /root/Desktop/scrapping_full/cron/seperate_cron/shopify_update.py
- You can direct standard output and error log to files
  - python3 your_script.py > log_file.txt 2>&1 -- Logs & errors going into log_file.txt
  - python3 your_script.py > stdout_log.txt 2> stderr_log.txt -- Logs going into stdout_log.txt and errors are in stderr_log.txt
  - python3 your_script.py >> stdout_log.txt 2>> stderr_log.txt -- Logs are **appended** to stdout_log.txt and errors are **appended** to stderr_log.txt

## [Known Issues](#known-issues)

- vsta_scrape_run Currently running locally because the website isn't loading in the server
- similarweb_run Currently running locally because the website isn't loading in the server
- In some cases, The actual code runnin
- **check if user credentials are hardocded in the scripts.**
  - in redit_cron.py, credentials are hardcoded in the code.
  - in creds - password is visible as text. This is used in module database connect to database.
  - vstat_cred - email passwords are exposed.
  - API key is hardcoded in the `save_ads_api_production`

## [Common Python Modules](#common-python-modules)

Below is a list of common/core python modules which are used in individual 'run' scripts. The core logic sits in these modules. The functions inside are called in the scripts to perform the necessary steps. Below table provides you a list of functions and a breif description of what it does.

| **index** | **Python Module**             | **Function Name**                 | **Description**                                                                                                                                                                                   |
| --------: | :---------------------------- | :-------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
|         1 | vstat_scrape                  | login                             | Logs in to VStat website using provided credentials and opens main dashboard.                                                                                                                     |
|         2 |                               | parse_data                        | Scrapes website data for brand and returns dictionary.                                                                                                                                            |
|         3 |                               | safe_execute                      | Executes a function and returns its output or default value if an exception occurs.                                                                                                               |
|         4 |                               | get_monthly_traffic               | Scrapes and returns monthly traffic data as JSON (visits and views).                                                                                                                              |
|         5 |                               | get_lastmonth_traffic             | Scrapes and returns website traffic data for previous month as JSON.                                                                                                                              |
|         6 |                               | get_traffic_sources               | Scrapes and returns website traffic sources data as JSON.                                                                                                                                         |
|         7 |                               | get_top_countries                 | Scrapes and returns dictionary of top countries with percentage share (JSON).                                                                                                                     |
|         8 |                               | get_social_sources                | Scrapes and returns dictionary of top social media sources with percentage share (JSON).                                                                                                          |
|         9 |                               | get_competitors                   | Scrapes and returns list of website competitors as JSON.                                                                                                                                          |
|        10 |                               | get_organic_keywords              | Scrapes and returns dictionary of organic keywords with percentage share (JSON).                                                                                                                  |
|        11 |                               | get_bounce                        | Attempts to scrape bounce rate and returns string or None.                                                                                                                                        |
|        12 |                               | get_page_per_visit                | Attempts to scrape average pages per visit and returns string or None.                                                                                                                            |
|        13 |                               | get_timeonsite                    | Attempts to scrape average time spent on site and returns string or None.                                                                                                                         |
|        14 |                               | get_paid_keywords                 | Scrapes and returns dictionary of paid keywords with percentage share (JSON).                                                                                                                     |
|        15 | trustpilot_reviews            | proxy_browser                     | The function sets up a headless Firefox WebDriver with proxy settings and performance configurations.                                                                                             |
|        16 |                               | save_master_trustpilot            | updates a record in the master_table with Trustpilot and brand information                                                                                                                        |
|        17 |                               | save_brand_trustpilot             | The function updates review details for a brand in the brand_table, using the most recent timestamp for that brand.                                                                               |
|        18 |                               | get_url                           | Extracts url paths and brand name from a row in the data.                                                                                                                                         |
|        19 |                               | search_brand                      | Searches for a brand in Trustpilot using the driver.                                                                                                                                              |
|        20 |                               | review_finder                     | Main function that iterates through brands, scrapes reviews, and stores them.                                                                                                                     |
|        21 | shopify_store_reviews         | data_connect                      | Connect to the database, execute the query, and return the results as a DataFrame                                                                                                                 |
|        22 |                               | country_description_data          | Fetches the country description and country name from a JSON file at the given URL                                                                                                                |
|        23 |                               | save_country_description_master   | Updates the country description and country name for a given brand in the master_table.                                                                                                           |
|        24 |                               | save_brand_reviews                | Updates the review count and rating for a brand in the brand_table.                                                                                                                               |
|        25 |                               | meta_data                         | Extracts Open Graph and Twitter meta properties from the page.                                                                                                                                    |
|        26 |                               | update_meta_properties            | Updates SEO meta properties and Twitter meta properties in the master_table.                                                                                                                      |
|        27 |                               | shopify_review                    | Retrieves and updates review data for a given Shopify brand from various review platforms.                                                                                                        |
|        28 | shopify_theme                 | shopify_currency_rate_data_master | Retrieves the currency and exchange rate from a Shopify store's meta data.                                                                                                                        |
|        29 |                               | save_currency_rate_master         | Updates the currency and exchange rate for a given brand in the master table.                                                                                                                     |
|        30 |                               | theme_parser                      | getting the theme of the shop                                                                                                                                                                     |
|        31 |                               | app_parser                        | getting the app extensions list                                                                                                                                                                   |
|        32 |                               | currency_parser                   | getting currency                                                                                                                                                                                  |
|        33 |                               | get_stored_app_data               | getting the app list that is already created                                                                                                                                                      |
|        34 |                               | parse_social_links                | getting social links                                                                                                                                                                              |
|        35 |                               | get_apps                          | finding which apps are in the precreated list and the others                                                                                                                                      |
|        36 | shopify_update                | get_top_best_seller               | Fetches up to 20 top best-selling products from a given Shopify store URL, handling pagination, timeouts, and errors.                                                                             |
|        37 |                               | fetch_published_products_count    | To get the published prouct count                                                                                                                                                                 |
|        38 |                               | getting_page_count                | To get the page count to scrape                                                                                                                                                                   |
|        39 |                               | get_page                          | process the json from shopify.com/products.json?page= and return list of products                                                                                                                 |
|        40 |                               | convert_datetime                  | This function attempts to convert a string to a datetime object using pandas                                                                                                                      |
|        42 |                               | extract_products_collection       | This function extracts product data from a paginated API, processes variants and images, and returns a consolidated DataFrame with cleaned and transformed data for further analysis.             |
|        43 |                               | extract_products                  | This function extracts product data from a URL, processes it, and inserts the data into a database in batches, with timing for extraction and ingestion operations.                               |
|        44 |                               | insert_data_in_batches            | Function to insert data in batches                                                                                                                                                                |
|        45 | save_brand_master             | mysql_login                       | Establishes a connection to the MySQL database and returns the connection and cursor.                                                                                                             |
|        46 |                               | data_connect                      | Reads data from the specified query in the MySQL database and returns a DataFrame.                                                                                                                |
|        47 |                               | save_master                       | Inserts data into the master_table to save Shopify site information for a brand. If the brand already exists, it skips.                                                                           |
|        48 | shopify_checker2              | master_db_login                   | Establishes a connection to the MySQL database and returns the connection and cursor.                                                                                                             |
|        49 |                               | data_connect                      | Reads data from the specified query in the MySQL database and returns a DataFrame.                                                                                                                |
|        50 |                               | save_shopify_url                  | Updates the ShopifySite field in the master_table with the provided Shopify URL for a specific brand.                                                                                             |
|        51 |                               | mysql_login                       | Establishes a connection to the MySQL database and returns the connection and cursor.                                                                                                             |
|        52 |                               | get_shopify_site                  | Attempts to fetch the Shopify site URL by appending '/products.json' to the given URL and sending an HTTP request. If unsuccessful, returns 'NULL'.                                               |
|        53 |                               | fetch_myshopify_url               | Fetches the Shopify URL from the page source of the given URL using a regex pattern. If unsuccessful, returns None.                                                                               |
|        54 |                               | get_redirect_url                  | Gets the redirect URL for the given Shopify URL. If there's no redirect or if an error occurs, returns the original URL.                                                                          |
|        55 | shopify_reviews_save_brand    | data_connect                      | Reads data from the specified query in the MySQL database and returns a DataFrame.                                                                                                                |
|        56 |                               | save_shopify_rating               | Updates the ShopifyReviewCount, ShopifyAvgRating, and ShopifyReviewsUpdatedTime fields in the master_table with the provided review count, average rating, and current date for a specific brand. |
|        57 | similarweb_scrape             | get_useragent                     | Randomly selects and returns a User-Agent string from a predefined list of User-Agent strings.                                                                                                    |
|        58 |                               | getdriver_proxyless               | Configures and returns a Chrome WebDriver instance with random proxy and user-agent.                                                                                                              |
|        59 |                               | extract_month                     | Extracts the month abbreviation from the input string.                                                                                                                                            |
|        60 |                               | close_overlay                     | Closes the overlay if present on the page.                                                                                                                                                        |
|        61 |                               | get_tooltip_contents2_new_None    | Collects tooltip contents from the chart on the page.                                                                                                                                             |
|        62 |                               | rank_finders_1                    | Extracts global, country, and category ranks from the provided BeautifulSoup object.                                                                                                              |
|        63 |                               | rank_finders_2                    | Extracts global, country, and category ranks from the provided BeautifulSoup object with a different HTML structure.                                                                              |
|        64 |                               | close_pop_up_1                    | Closes a pop-up window by clicking on the close button identified by its XPath.                                                                                                                   |
|        65 |                               | close_pop_up_2                    | Closes a pop-up window inside an iframe by first switching to the iframe and then clicking the close button.                                                                                      |
|        66 |                               | similarwebscrapping               | Extracting the trafic data and save to similarweb_data table                                                                                                                                      |
|        67 | redit_cron                    | save_brand_redit                  | Updates the brand_table with the count of Reddit mentions for a specific brand.                                                                                                                   |
|        68 | database_connect              | get_connection                    | Establishes a connection to the MySQL database using the provided credentials and returns the connection and cursor.                                                                              |
|        69 |                               | close_connection                  | Closes the connection to the MySQL database.                                                                                                                                                      |
|        70 |                               | master_db_login                   | Connects to the master database using MySQL and returns the connection and cursor objects.                                                                                                        |
|        71 |                               | get_proxy                         | Retrieves a list of proxy information (login, password, proxy) from the fb_account_proxies_merged table in the facebook_feed database.                                                            |
|        72 |                               | get_useragent                     | Returns a randomly selected user-agent string from a predefined list.                                                                                                                             |
|        73 |                               | getdriver                         | Configures and returns a headless Chrome WebDriver with specified options, user-agent, and proxy.                                                                                                 |
|        74 |                               | waitfor                           | Waits for a specified element to be present on the web page before continuing execution.                                                                                                          |
|        75 |                               | jsclick                           | Uses JavaScript to click on a specified element on the web page.                                                                                                                                  |
|        76 |                               | scrollDown                        | Scrolls down the web page to load additional content dynamically.                                                                                                                                 |
|        77 |                               | fix_url                           | Ensures that a given URL is properly formatted with the correct protocol (http/https).                                                                                                            |
|        78 |                               | shopify_master_only               | Connects to the master database, executes the provided query, and returns a DataFrame with the fetched data.                                                                                      |
|        79 | domain_search                 | save_results                      | Updates the OtherDomains field in the shopify_theme table for a specific brand with the given results.                                                                                            |
|        80 |                               | data_connect                      | Reads data from the MySQL database using the specified query and returns a DataFrame.                                                                                                             |
|        81 |                               | check_url                         | Checks if a given URL is working and whether it is a Shopify URL by attempting to access the /products.json endpoint.                                                                             |
|        82 |                               | perform_web_requests              | Performs multithreading to load top-level domains (TLDs) into a queue and initiates web requests to discover subdomains.                                                                          |
|        83 | social_metric(ads_library_lf) | setup_logging                     | Create a unique logger for each process                                                                                                                                                           |
|        84 |                               | mysql_login                       | Establishes a connection to the MySQL database and returns the connection and cursor objects.                                                                                                     |
|        85 |                               | last_value                        | Get the first value of a specified column for a given page_id from the DataFrame.                                                                                                                 |
|        86 |                               | extract_about_text                | extracting the about text from the html tag                                                                                                                                                       |
|        87 |                               | extract_page_category             | extracting the page category value from html tag                                                                                                                                                  |
|        88 |                               | extract_likes                     | extracting the likes value from html tag                                                                                                                                                          |
|        89 |                               | extract_ig_followers              | extracting the instagram followers value from html tag                                                                                                                                            |
|        90 |                               | extract_brand_name                | extracting the brand name value                                                                                                                                                                   |
|        91 |                               | extract_fb_url                    | extracting the facebook page url                                                                                                                                                                  |
|        92 |                               | extract_admin_countries           | extarcting the admin countries with count value                                                                                                                                                   |
|        93 |                               | extract_page_created_time         | extarcting the page created value                                                                                                                                                                 |
|        94 |                               | savedata_brand_table              | saving the data to brand_table                                                                                                                                                                    |
|        95 |                               | update_data                       | updating the data into master_table                                                                                                                                                               |
|        96 |                               | scrape_and_extract                | Scrapes the page source and extracts various information.                                                                                                                                         |
|        97 |                               | scrape_pages                      | Scrape data for each page_id using a proxy and log the results                                                                                                                                    |
|        98 | save_ads                      | proxy_browser                     | Creates and returns a Chrome WebDriver instance configured with a specified proxy server and optimized settings.                                                                                  |
|        99 |                               | waitfor                           | Waits up to 9 seconds for an element with the given XPath to appear.                                                                                                                              |
|       100 |                               | jsclick                           | Waits for the element with the given XPath to be present and then clicks it using JavaScript.                                                                                                     |
|       101 |                               | scrollDown                        | Scrolls down the page until reaching the end, checking if the page height changes.                                                                                                                |
|       102 |                               | mysql_login                       | Establishes a connection to the MySQL database and returns the connection and cursor objects                                                                                                      |
|       103 |                               | last_value                        | Get the first value of a specified column for a given page_id from the DataFrame.                                                                                                                 |
|       104 |                               | json_formatting                   | Formats JSON data by removing the 'is_aaa_eligible' key and renaming specific keys                                                                                                                |
|       105 |                               | remove_backslashes                | Removes backslashes from strings in a list or dictionary.                                                                                                                                         |
|       106 |                               | ensure_cards_structure            | Ensures that the 'cards' in the provided data have a consistent structure with all required keys.                                                                                                 |
|       107 |                               | convert_to_string                 | Recursively converts specific values in the input JSON data to strings                                                                                                                            |
|       108 |                               | replace_none_with_empty_string    | Recursively replaces `None` values with empty strings in the input data.                                                                                                                          |
|       109 |                               | update_snapshot                   | Update 'body' structure                                                                                                                                                                           |
|       110 |                               | update_additional_fields          | updating additional fields                                                                                                                                                                        |
|       111 |                               | extract_ad_library_main           | Extracts the text between the markers '"edges":' and '"page_info":{"end_cursor"'.                                                                                                                 |
|       112 |                               | extract_urls_and_ids              | Extracts URLs and request IDs from ad log entries                                                                                                                                                 |
|       113 |                               | fetch_and_filter_json             | Fetches JSON response bodies for given request IDs and filters those containing 'ad_archive_id'.                                                                                                  |
|       114 |                               | process_json_list                 | Processes a list of JSON strings to extract and clean data, then returns a combined list of results.                                                                                              |
|       115 |                               | combine_ads_from_full_list        | Combines ads from a list of JSON objects by extracting and aggregating ad data.                                                                                                                   |
|       116 |                               | get_unique_ads                    | Filters out duplicate ads based on 'ad_archive_id', returning a list of unique ads.                                                                                                               |
|       117 |                               | correct_format_and_types_updated  | Ensures that `test_payload` matches the format and types of `correct_payload`.                                                                                                                    |
|       118 | shopify_best_seller           | get_top_best_seller_new           | This function retrieves the top 20 best-selling products from a paginated URL by parsing the product data from the page source                                                                    |
|       119 |                               | update_product_ranks              | Updates the product rankings in the database based on the top best-selling products from the given URL.                                                                                           |
|       120 | dropship_update               | mysql_login                       | Connects to the MySQL database and returns the connection and cursor.                                                                                                                             |
|       121 |                               | data_connect                      | Fetches all data from the specified table and returns it as a DataFrame.                                                                                                                          |
|       122 |                               | proxy_browserF                    | Configures and returns a headless Firefox WebDriver with proxy settings and browser options.                                                                                                      |
|       123 |                               | get_main_domain                   | Clean the URL by removing backslashes                                                                                                                                                             |
|       124 |                               | update_dropshippers               | update dropship value to master_table                                                                                                                                                             |
|       125 | update_insta_urls             | get_soup                          | Fetches the HTML content from the given URL and parses it with BeautifulSoup.                                                                                                                     |
|       126 |                               | extract_instagram_urls            | Extracts Instagram URLs from the given page source using regex.                                                                                                                                   |
|       127 |                               | extract_instagram_urls_2          | Extracts Instagram URLs from the given page source using a regex pattern.                                                                                                                         |
|       128 |                               | save_insta_url                    | Updates the Instagram URL for a given brand ID in the master_table.                                                                                                                               |
|           |

## [Details of Scripts](#details-of-scripts)

### 1. shopify_update

- **Function:** Find new products of each brand from Shopify store
- **Schedule:** Currently not scheduled,running in every 1-2 months for all shopify_products new tables (1 to ..x)
- **Host Server:** 209.145.48.140
- **Path to script:** `python3 /root/Desktop/shopify_products/shopify_products_optimized_run.py
- **Steps to execute (manually):** Connect to the host server provided above and navigate to the script path or just directly type `python3 /root/Desktop/shopify_products/execute_many_batches_optimized_run.py`
- **Logs:** logs/optimized_execute_many{date}.log
- **Related Custom Python Packages/Files:** shopify_products_optimized, database_connect
- **Additional Notes:**
  - Runs on a single server
  - Reads the master_table from a database connection using pandas.
  - Drops duplicate brands and resets the index.
  - Extracts brands with non-null "BrandSite" and "BrandName" values.
  - Calls the `extract_products` function from the `execute_many_optimized_batches` module to gather product details from the respective Shopify website.
  - Saves the extracted products and update the brand's Shopify information in the `master_table`.

---

### 2. redit_cron

- **Function:** Get Reddit mentions for each brand
- **Schedule:** Currently scheduled to run every Tuesday at midnight.
- **Host Server:** 207.244.246.21, 207.244.237.135, 209.145.59.158
- **Path to script:** `python3 /root/Desktop/scrapping_full/cron/separate_cron/redit_cron.py`
- **Steps to execute (manually):** Connect to the host server provided above and navigate to the script path or just directly type `python3 /root/Desktop/scrapping_full/cron/separate_cron/redit_cron.py`
- **Logs:** Logs are stored at logs/redit*update*{date}.log
- **Related Custom Python Packages/Files:** reddit_creds
- **Additional Notes:**
  - Runs on multiple servers.
  - Connects to the "master_db" using `master_db_login`.
  - Retrieves a list of brands from the `shopify_master_only` function
  - Authenticates with the Reddit API using provided credentials.
  - Iterates through each brand in the list.
  - Searches Reddit's "all" subreddit for posts containing the brand name hashtag.
  - Iterates through each retrieved submission and extracts its content.
  - Processes the content: Encodes and decodes to remove non-ASCII characters. Tokenizes the text into sentences using NLTK's Punkt tokenizer.
  - At this point, the code identifies the mentions using a regex. Only sentences with identified brand are stored. Repeated sentences are removed.
  - `brand_table` with total number of mentions for each brand is updated.
  - `redit_mentions` table is also updated for each mention/sentence.

---

### 3. vstat_scrape

- **Function:** Get brand store analytic data from Vstat
- **Schedule:** Currently scheduled to run every Friday at midnight on server .21 and .135 and runs 7PM every Friday on .128.
- **Host Server:** 207.244.246.21, 207.244.237.135, 207.244.238.128
- **Path to script:** `python3 /root/Desktop/scrapping_full/cron/separate_cron/vstat_scrape_run.py`
- **Steps to execute (manually):** Connect to the host server provided above and navigate to the script path or just directly type `python3 /root/Desktop/scrapping_full/cron/separate_cron/vstat_scrape_run.py`
- **Logs:** logs/vstat_update{date}.log
- **Related Custom Python Packages/Files:** vstat_scrape (main module), vstat_cred
- **Additional Notes:**
  - Runs on multiple servers
  - Apart from other libraries, imports `vstat_scrape` custome module. Functions defined in this module are used by this script.
  - Extracts a list of brands using `shopify_master_only` function
  - Creates a subset of 100 to 200 **Not clear if this needs to be changed everytime we run the scripts**
  - Creates `login_url` and sets up `VstatLoginDriver` using passwords and email provided in 'vstat_cred.py' and creates a session.
  - Iteratively, using the brand name, constructs `vstat.info URL` for crawling and scraping the data.
  - Every 25 iterations, the process quits and waits for 10 mins to avoid bot detection. Afterwards it resumes by initializing a new driver.
  - The scraped data is stored in `VstatScrape` object and parses through different traffic data sections.
  - Builds a data frame from the extracted data and then connect to the db using `master_db_login`
  - Creates an insert statement for table `vstat_analystics`
  - To avoid detection, proxyless scraping techinique is used. If script encounters an error, it skips over the brand and moves to the next one.

---

### 4. trustpilot_review_updated_run

- **Function:** Get Trustpilot reviews and other brand details for each brand
- **Schedule:** Currently scheduled to run every Wednesday at midnight.
- **Host Server:** 207.244.246.21, 207.244.237.135, 207.244.238.128
- **Path to script:** `python3 /root/Desktop/scrapping_full/cron/separate_cron/trustpilot_review_updated_run.py`
- **Steps to execute (manually):** Connect to the host server provided above and navigate to the script path or just directly type `python3 /root/Desktop/scrapping_full/cron/separate_cron/trustpilot_review_run.py`
- **Logs:** logs/trustpilot*update*{date}.log
- **Related Custom Python Packages/Files:** trustpilot_reviews_updated
- **Additional Notes:**
  - Runs on multiple servers.
  - Apart from other libraries, imports `trustpilot_reviews` custome module. Functions defined in this module are used by this script.
  - A list of brands is retrived via function `shopify_master_only`
  - Calls the `review_finder` from `trustpilot_reviews` module to actually scrape the data.
  - In the current version of the code, the brand name is hardcoded to 'Vessi'. Not clear, if one has to run, we need to run for a specific brand only or a number brands can be passed. There was an attempt to use a CSV to filter the brnads but that logic is commented out at the moment.

---

### 5. shopify_store_reviews_updated_run

- **Function:** Get Shopify brand reviews from sites like Loox, Judge.me, etc.
- **Schedule:** Currently scheduled to run every Tuesday at midnight on .21 & .135 and 5AM every Monday on .158 server.
- **Host Server:** 207.244.246.21, 207.244.237.135, 209.145.59.158
- **Path to script:** `python3 /root/Desktop/scrapping_full/cron/separate_cron/shopify_store_reviews_updated_run.py`
- **Steps to execute (manually):** Connect to the host server provided above and navigate to the script path or just directly type `python3 /root/Desktop/scrapping_full/cron/separate_cron/shopify_store_reviews_run.py`
- **Logs:** log files are created `logs/shopify_store_reviews_{date}.log`
- **Related Custom Python Packages/Files:** `shopify_store_reviews`
- **Additional Notes:**
  - Gathers the brand name and Shopify site URL.
  - Calls the `shopify_review` function from the `shopify_store_reviews_updated`
  - Maintains all the reviews in a variable `df_full` by continually concatenating.
  - Core logic to extract the review sits in the `shopify_review` function.

---

### 6. similarweb_new_run

- **Function:** Collecting website analytic data to SimilarWeb data table
- **Schedule:** Currently not scheduled. We run it on 11 th of every month
- **Host Server:** 95.111.230.152, 209.145.59.158, 207.244.237.135
- **Path to script:** `python3 /root/Desktop/scrapping_full/cron/separate_cron/similarweb_run.py`
- **Steps to execute (manually):** Connect to the host server provided above and navigate to the script path or just directly type `python3 /root/Desktop/scrapping_full/cron/separate_cron/similarweb_run.py`
- **Logs:** Logs are stoed at logs/similarweb*update*{date}.log
- **Related Custom Python Packages/Files:** similarweb_scrapping
- **Additional Notes:**
  - Runs on multiple servers.
  - This script gets the brands from `shopify_master_only` function.
  - Resets the index of `similarweb_brands` data frame.
  - Calls 'similarwebscrapping' function from the 'similarweb_scrapping' module for the entire list of brands.
  - The scrapping function extracts different data points for each brand website such as overall ranking, country ranking, etc.
  - Once done, the script writes everything into database. The target table name is 'similarweb_data'

---

### 7. save_brand_master

- **Function:** Save all new brands from master_table_2 to master_table
- **Schedule:** Currently scheduled to run every day at 19:01.
- **Host Server:** 207.244.246.21
- **Path to script:** `python3 /root/Desktop/scrapping_full/cron/separate_cron/save_brands_master.py`
- **Steps to execute (manually):** Connect to the host server provided above and navigate to the script path or just directly type `python3 /root/Desktop/scrapping_full/cron/separate_cron/save_brands_master.py`
- **Logs:** Logs are stored at logs/new_brands_save_brand{date}.log
- **Related Custom Python Packages/Files:** No dependency on other modules
- **Additional Notes:**
  - This script basically updates the `master_table` from the data extracted and saved in `master_table_2`
  - The functionlity is very simple, reads every brand name, facebook url, shopify site and page id from the `master_table_2` and checks if pageid already exists which means brand already exists so it should be skipped.
  - if it can't find the pageid, then it saves the brand to mater_table because it is a new brand which never existed in the system before.
  - It is important to note that the logic relies on pageid. **should validate if page id of a brand can change?**

---

### 8. shopify_reviews_save_brand

- **Function:** Run Shopify review save brand every Saturday at 17:00.
- **Schedule:** Currently scheduled to run every Saturday at 17:00.
- **Host Server:** 207.244.246.21
- **Path to script:** `python3 /root/Desktop/scrapping_full/cron/separate_cron/shopify_reviews_save_brand.py`
- **Steps to execute (manually):** Connect to the host server provided above and navigate to the script path or just directly type `python3 /root/Desktop/scrapping_full/cron/separate_cron/shopify_reviews_save_brand.py`
- **Logs:** Logs are stored at logs/shopify_reviews_save_brand{date}.log
- **Related Custom Python Packages/Files:** shopify_reviews
- **Additional Notes:**
  - This script ultimately updates the `brand_table` with review count and rating information.
  - using `data_connect` function to execute a SQL query and retrieve Shopify review data from `shopify_reviews2`
  - data is prepared in 2 data frames `brand_df` and `latest_reviews`
  - calls a function `save_brand_trustpilot` function to update the brand_table for review count and average rating.

---

### 9. freightos_new_run2

- **Function:** Collecting Freightos indices from the Freightos website.
- **Schedule:** Currently scheduled to run daily at 04:10 AM.
- **Host Server:** 207.244.246.21
- **Path to script:** `python3 /root/Desktop/scrapping_full/cron/freightos_new_run2.py`
- **Steps to execute (manually):** Connect to the host server provided above and navigate to the script path or just directly type `python3 /root/Desktop/scrapping_full/cron/freightos_new_run2.py`
- **Logs:** Logs are stored at logs/Freightos*indices*{date}.log
- **Related Custom Python Packages/Files:** No dependency on other modules
- **Additional Notes:**
  - Don't think it is being used. **Need to Double Check**

---

### 10. shopify_checker2

- **Function:** Check whether the added brand is Shopify.
- **Schedule:** On demand.
- **Host Server:** 207.244.246.21
- **Path to script:** `python3 /root/Desktop/scrapping_full/cron/shopify_checker2.py`
- **Steps to execute (manually):** Connect to the host server provided above and navigate to the script path or just directly type `python3 /root/Desktop/scrapping_full/cron/shopify_checker2.py`
- **Logs:** Logs are stored at logs/shopify*checkerlog*{date}.log
- **Related Custom Python Packages/Files:** No dependency on other modules
- **Additional Notes:**
  - The core purpose of this script is to update the shopify urls (if it is a shopify store).
  - This is achieved by first selecting all the brands where the Shopify URL is empty/NULL.
  - Then URLs are extracted in two ways:
    - By accessing the brand's website and parsing the JSON response from /products.json (using `get_shopify_site`).
    - By finding a URL matching the two-pillars.myshopify.com format in the website HTML (using `fetch_myshopify_url`).
  - Then calls `save_shopify_url` to update the records in `master_table`
  - It is important to note that the script has various parts commented out, so it is possible that the code that is running on the server may be different to the version checked into Git.

---

### 16. shopify_theme_updated_run

- **Function:** Get Shopify theme, apps used, other domain, social media links from Shopify store site
- **Schedule:** Currently scheduled to run at 5:00 PM every Saturday.
- **Host Server:** 207.244.237.135
- **Path to script:** `python3 /root/Desktop/scrapping_full/cron/separate_cron/shopify_theme_run.py`
- **Steps to execute (manually):** Connect to the host server provided above and navigate to the script path or just directly type `python3 /root/Desktop/scrapping_full/cron/separate_cron/shopify_theme_run.py`
- **Logs:** logs/shopify*theme_update*{date}.log
- **Related Custom Python Packages/Files:** shopify_theme
- **Additional Notes:**
  - This script imports `shopify_theme` module
  - Reads brands by calling `shopify_master_only` function.
  - Creates an object of `ShopifyMetaScraper` for the brand url.
  - then uses `theme_parser` and `get_apps` to parse the theme.
  - dumps the json for the apps and other apps into variables and constructs a sql to update the table `shopify_theme`

---

### 23. domain_search

- **Function:** The script searches for any alternate domains mentioned against each brand
- **Schedule:** Currently scheduled to run at 9:00 AM every Thursday.
- **Host Server:** 207.244.238.128
- **Path to script:** `python3 /root/Desktop/scraping_full/cron/Scripts/DOMAIN_SEARCH/domain_search.py`
- **Steps to execute (manually):** Connect to the host server provided above and navigate to the script path or just directly type `python3 /root/Desktop/scraping_full/cron/Scripts/DOMAIN_SEARCH/domain_search.py`
- **Logs:** logs/domain*search*{date}.log
- **Related Custom Python Packages/Files:** No dependency on other modules
- **Additional Notes:**
  - The script starts with reading the brands from the `shopify_theme` table and extracts the domain ame from the Shopify URL.
  - Creates a multi threaded worker queue (15 by default) to loops through a list of top level domains (TLD)
  - For every TLD, creates a potential subdomain URL such as subdomain.TLD or TLD/subdomain and add every potential URL to the queue.
  - The worker thread then checks if the url exists and has Shopify products, it so then it is saved and if not url is ignore.
  - Once worker tasks are done, the data is de-duplicated and converted into JSON and save in the table `shopify_theme` in the column `OtherDomains`

---

### 25. save_ads_new_method

- **Function:** Get page details of each brand from ads library, Get ad details of each ad from ads library, Update ad details, and save ad image to AWS and ad videos to Wasabi storage
- **Schedule:** Daily, once the previous run completes.
- **Host Server:** 207.244.239.107
- **Path to script:** `python3 /root/Desktop/FB_SCRAPERS/save_ads_new_method.py
- **Steps to execute (manually):** Connect to the host server provided above and navigate to the script path or just directly type `python3 /root/Desktop/FB_SCRAPERS/save_ads_new_method.py
- **Logs:** logs/save_ads_new_method{date}
- **Related Custom Python Packages/Files:** correct_json
- **Additional Notes:**
  - This scripts navigates to Facebook ad library URLs for target pages and countries.
  - Parses network logs and DOM elements to extract ad JSON data.
  - Formats and cleans the extracted ad data.
  - Uses multiple chrome instances with proxies to perform parallel scraping.
  - Sends formatted ad data to TrendRocket API endpoints for storage.

---

### 26. ads_library_lf_updated

- **Function:** Get page details of each brand from ads library
- **Schedule:** Daily, once the previous run completes.
- **Host Server:** 207.244.239.107
- **Path to script:** `python3 /root/Desktop/FB_SCRAPERS/ads_library_lf_updated`
- **Steps to execute (manually):** Connect to the host server provided above and navigate to the script path or just directly type `python3 `python3 /root/Desktop/FB_SCRAPERS/ads_library_lf_updated`
- **Logs:** logs/ads_library_lf_updated{date}
- **Related Custom Python Packages/Files:** No dependency on custom modules
- **Additional Notes:**
  - This scThe script fetches a list of page IDs from the database.
  - It creates multiple Chrome browser instances, each using a different proxy from a pool.
  - It iterates through the list of page IDs and for each page ID:
    - Chooses a driver from the available pool (round-robin approach).
    - Navigates to the Facebook Ads Library search page for that page ID.
    - Extracts various information like category name, brand website, admin countries, etc., from the network logs and page source.
    - Updates the database table with the extracted information.
    - Clears the browser cache to avoid detection.
  - Following functions are created and used in the script:
    - `proxy_browser`: Creates a Chrome browser instance with a specified proxy.
    - `get_proxy`: Fetches proxy login credentials from a database.
    - `login_to_facebook`: Logs into Facebook using provided login credentials.
    - `waitfor`: Waits for a specific element to appear on the webpage.
    - `jsclick`: Clicks on a specific element using JavaScript.
    - `scrollDown`: Scrolls down the webpage.
    - `logout`: Logs out of Facebook.
    - `mysql_login`: Connects to a MySQL database.
    - `get_page`: Fetches a list of page IDs from the database.
    - `admin_countries_with_counts_X`: Extracts admin countries and their respective counts from the page source using regular expressions.
    - `last_value`: Retrieves the last recorded value of a specific column for a given page ID from the database.
    - `extract_likes_from_page_source`: Extracts the number of page likes from the page source using a regular expression.
    - `extract_followers_from_page_source`: Extracts the number of Instagram followers from the page source using a regular expression.
    - `extract_page_info`: Extracts various information like category name, brand website, admin countries, etc., from the network logs and page source
    - `savedata_brand_table`: Saves the extracted page likes and Instagram followers to a database table.
    - `update_data`: Updates the database table with the extracted information about the page.
    - `clean_invalid_utf8`: Cleans invalid UTF-8 characters from a string.
    - `delete_cache`: Clears the browser cache.
    - `delete_cache_again`: Clears the browser cache again (possibly for additional cleanup).

---

### 27. shopify_best_seller

- **Function:** Get the best sellers of shopify brands and assign (1-20) ranks and update in the shopify_products table's ProductRank column.
- **Schedule:** Runs as requires
- **Related Custom Python Packages/Files:** No dependency on custom modules
- **Path to script:** `python3 /root/Desktop/shopify_products/shopify_best_seller_run.py.

---

### 28. dropship_update

- **Function:** Check whether a brand dropship or not and update in master_table.
- **Schedule:** Runs as requires
- **Related Custom Python Packages/Files:** dropship_list
- **Path to script:** python3 /root/Desktop/scraping_full/cron/Scripts/DROPSHIP/update_dropshippers.py

---

### 28. UPDATE_INSTAGRAM_URL

- **Function:** Fetch the insta urls of brands from page source and update it in the master_table.
- **Schedule:** Runs as requires
- **Related Custom Python Packages/Files:** No dependency on custom modules
- **Path to script:** python3 /root/Desktop/scrapping_full/cron/get_insta_urls.py
