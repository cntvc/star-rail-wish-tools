# flake8: noqa
en_us_lang_pack = {
    # config
    "config.settings.current_status": "Current Status",
    "config.settings.open_success": "Opened successfully",
    "config.settings.close_success": "Closed successfully",
    # i18n
    "i18n.update_lang.tips": "The language changes will take effect after restarting. Do you want to continue? y/N",
    "i18n.update_lang.invalid_input": "Please enter a valid option. Only 'y' or 'N' are allowed.",
    # module/mihoyo/account
    "account.login_account_success": "Successfully set account: {}",
    "account.invalid_cookie": "No valid Cookie data detected",
    "account.add_account_success": "Account added successfully, UID: {}",
    "account.update_cookie_success": "Successfully updated account Cookie, UID: {}",
    "account.current_account": "Current account {}",
    "account.without_account": "No account currently set",
    "account.menu.select_account": "Select account: {}",
    "account.menu.add_by_game_uid": "Enter game UID to add account",
    "account.menu.add_by_cookie": "Add account via Cookie",
    "account.menu.input_uid": "Please enter user UID, enter 0 to cancel creating a new user\n",
    "account.menu.invalid_uid_format": "Please enter a valid UID format",
    # module/record/client
    "record.client.fetch_record": "Fetching records",
    "record.client.fetch_msg": "\033[KFetching {} banner data {}",
    "record.client.fetch_finish": "\033[KFetch of {} finished, {} data entries in total",
    "record.client.analyze_update_time": "Analyzing update time: ",
    "record.client.invalid_gacha_url": "No valid gacha link found",
    "record.client.record_info_data_error": "Error in account storage data, record_info_uid: {}",
    "record.client.diff_account": "Current game account is different from software account, export not possible",
    "record.client.account_no_record_data": "No gacha records for the account",
    "record.client.invalid_srgf_data": "File {} is not in standard SRGF format, this import will be ignored",
    "record.client.diff_account_srgf_data": "Data in file {} does not belong to the current account, this import will be ignored",
    "record.client.import_file_success": "File {} imported successfully",
    "record.client.no_file_import": "No valid data file recognized",
    "record.client.export_file_success": "Export successful, file is located at {} ",
    # module/game_client
    "game_client.unfind_game_log_file": "Game log file not found",
    "game_client.unfind_game_path": "Game path not found",
    "game_client.unfind_game_cache_file": "Game web cache file not found",
    # module/info
    "info.app_name": "App Name: ",
    "info.project_home": "Project Home: ",
    "info.author": "Author: ",
    "info.email": "Email: ",
    "info.app_version": "App Version: {}",
    # module/updater
    "updater.invalid_input": "Please enter a valid option. Only 'y' or 'N' are allowed.",
    "updater.download_failed": "Failed to download the new version file. Please check the network connection status.",
    "updater.download_success": "New version download completed: {}, the software will automatically restart shortly.",
    "updater.check_update": "Checking for software updates...",
    "updater.check_update_net_error": "Failed to check for updates. Please check the network connection status.",
    "updater.check_update_has_no_info": "Failed to check for updates. No version information obtained.",
    "updater.is_latest_version": "The current version is already the latest.",
    "updater.upgrade_success": "Software update successful. Current version: {}\n",
    "updater.delete_file_failed": "Failed to delete the old version file. Please manually delete the file: {}",
    "updater.changelog": "Changelog:",
    "updater.update_option": "New version {} detected. Do you want to update? y/N ",
    "updater.get_changelog_failed": "Failed to retrieve the changelog.",
    "updater.select_update_source": "Update source has been changed to {}",
    "updater.update_source_status": "Current update source is",
    # utils/menu
    "utils.menu.return_to_pre_menu": "0. Return to the previous menu",
    "utils.menu.exit": "0. Exit",
    "utils.menu.input_number": "Please enter a number to select a menu option:",
    "utils.menu.invalid_input": "This is an invalid input. Please try again.",
    # client
    "client.no_account": "No account found",
    "client.empty_cookie": "No cookies found, please set cookies and retry",
    # main-menu
    "main.menu.main_menu.home": "Main Menu",
    # main-menu-account
    "main.menu.account_setting": "Account Settings",
    # main-menu-gacha_record
    "main.menu.gacha_record.home": "Gacha Records",
    "main.menu.refresh_record_by_game_cache": "Fetch Using Game Cache",
    "main.menu.refresh_record_by_clipboard": "Fetch Using Clipboard",
    "main.menu.refresh_record_by_user_cache": "Fetch Using App Cache",
    "main.menu.export_record_to_xlsx": "Export to Excel Spreadsheet",
    "main.menu.export_record_to_srgf": "Export to SRGF Generic Format File",
    "main.menu.import_gacha_record": "Import Gacha Records",
    "main.menu.show_analyze_result": "View Analysis Results",
    # main-menu-trailblaze_calendar
    "main.menu.trailblaze_calendar.home": "Trailblaze Calendar",
    "main.menu.trailblaze_calendar.fetch": "Fetch Trailblaze Calendar",
    "main.menu.trailblaze_calendar.show_history": "View History",
    # main-menu-setting
    "main.menu.settings.home": "Software Settings",
    "main.menu.settings.auto_update": "Auto Update",
    "main.menu.settings.update_source": "Set Update Source",
    "main.menu.settings.update_source_coding": "Coding (Recommended for users in China)",
    "main.menu.settings.update_source_github": "Github",
    "main.menu.settings.language": "Switch Language",
    "main.menu.about": "About...",
    # 分析结果总览表
    "table.total.title": "Analysis Results",
    "table.total.project": "Project",
    "table.total.total_cnt": "Total Count",
    "table.total.star5_cnt": "Total 5-Star Count",
    "table.total.star5_avg_cnt": "Average 5-Star Count",
    "table.total.pity_cnt": "Pity Count",
    # 5 星详情表
    "table.star5.title": "5-Star Details",
    "table.star5.pull_count": "th Pull",
    # 开拓月历
    "table.trailblaze_calendar.title": "Trailblaze Calendar",
    "table.trailblaze_calendar.month": "Date",
    "table.trailblaze_calendar.hcoin": "Stellars",
    "table.trailblaze_calendar.rails_pass": "Passes",
    # Execl
    "execl.header.time": "Time",
    "execl.header.name": "Name",
    "execl.header.type": "Type",
    "execl.header.level": "Rarity",
    "execl.header.gacha_type": "Gacha Type",
    "execl.header.total_count": "Total Count",
    "execl.header.pity_count": "Pity Count",
    # common
    "common.open": "Open",
    "common.close": "Close",
    # 卡池
    "regular_warp": "regular warp",
    "starter_warp": "starter warp",
    "character_event_warp": "character event warp",
    "light_cone_event_warp": "light cone event warp",
    # 异常
    "error.param_type_error": "Parameter type error, type: {}",
    "error.db_conn_error": "Database connection error",
    "error.request_error": "Network connection exception",
    "error.invalid_cookie_error": "Invalid Cookie",
    "error.authkey_error": "Link error",
    "error.invalid_authkey_error": "Invalid link",
}
