import mysql.connector
from mysql.connector.cursor import MySQLCursorBuffered
from rdsConnectAzure import *
import argparse

# parser = argparse.ArgumentParser(description="Arguments")
#
# parser.add_argument('--env', required=True, help='Environemt e.g., pa, prod, etc')
# parser.add_argument('--brand_name', required=True, help='Enter the brand name as per DB')
#
# args = parser.parse_args()

env = "local"

main_config_mapper = {  # env ---> config-main db
    "prod" : "config_store",
    "beta" : "config_store_beta",
    "qa2" : "config_store_qa2",
    "qa" : "config_store_qa",
    "perf" : "config_store_perf",
    "local" : "config_store_local"
}

conf_secrets, main_secrets = get_secret(main_config_mapper[env])

conn = mysql.connector.connect(
    host=main_secrets["host"],
    user=main_secrets["username"],
    password=main_secrets["password"],
    database=main_secrets["dbname"],
    use_pure=True  # <-- ensures Python implementation is used
)

conn_conf_store = mysql.connector.connect(
    host=conf_secrets["host"],
    user=conf_secrets["username"],
    password=conf_secrets["password"],
    database=conf_secrets["dbname"],
    use_pure=True  # <-- ensures Python implementation is used
)

# ✅ Use MySQLCursor explicitly to support multi=True
cursor = conn.cursor(cursor_class=MySQLCursorBuffered)
cursor_conf = conn_conf_store.cursor(cursor_class=MySQLCursorBuffered)

# brand_name = "ResultsCX" # DB ke hisaab se rakhna hai

def query_execution(con, sql, cursur):

    sql_statements = [stmt.strip() for stmt in sql.split(';') if stmt.strip()]

    zendesk_user_email = ""
    zendesk_user_name = ""
    brand_admin_id = None
    brand_id = -1

    try:

        con.start_transaction()
        for stmt in sql_statements:
            cursur.execute(stmt)
            print(f"Query executed: {stmt[:30]}...")
            print(f"Affected rows: {cursur.rowcount}")

            if stmt.startswith("SELECT @zendesk_user AS"):
                result = cursur.fetchone()
                if result:
                    zendesk_user_email = result[0]
                    zendesk_user_name = result[1]
                    print(zendesk_user_email, zendesk_user_name)

            if stmt.startswith("SELECT @CREATEDBY"):
                result = cursur.fetchone()
                if result:
                    brand_admin_id = result[0]
                    print(brand_admin_id)

            if stmt.startswith("SELECT @BRANDID"):
                result = cursur.fetchone()
                if result:
                    brand_id = result[0]
                    print(brand_id)

        con.commit()

    except Exception as e:
        con.rollback()
        print(f"❌ Transaction failed. Rolled back all changes.\nError: {e}")

    finally:
        cursur.close()
        # cursor_conf.close()
        con.close()
        # conn_conf_store.close()
        return zendesk_user_email, zendesk_user_name, brand_admin_id, brand_id

def get_variables(brand_name):

    sql = f"""

            SET @brandName := "{brand_name}";

            SET @brand_id = (SELECT id FROM brand WHERE name = @brandName);
            SET @account_id = (SELECT id FROM account WHERE brandName = @brand_id AND name = @brandName);
            SET @BRANDADMIN = (SELECT email FROM user WHERE account_id = @account_id AND firstName LIKE "%Brand%" AND lastName LIKE "%Admin%");
            SET @ACCOUNTID = (SELECT id FROM account WHERE name = @brandName);
            SET @BRANDID = (SELECT id FROM brand WHERE name = @brandName);
            SET @CREATEDBY = (SELECT id FROM user WHERE email = @BRANDADMIN);

            SELECT @BRANDID;
            SELECT @CREATEDBY;

            -- Zendesk Email
            SET @brand_url = (SELECT url FROM brand WHERE name = @brandName);
            SET @zendesk_user = CONCAT(SUBSTRING_INDEX(@brand_url, '.', 1), '.zendesk@zenarate.com');

            SELECT @zendesk_user AS zendesk_user_email, @brandName AS zendesk_user_name;

        """

    zendesk_user_email, zendesk_user_name, brand_admin_id, brand_id = query_execution(conn, sql, cursor)

    # config_store_sql = f"""
    #
    #             INSERT INTO brands_config (
    #                 brand_id, config_type, enabled, config_json, mapper, status,
    #                 created_at, created_by, updated_at, updated_by, deleted_at, deleted_by
    #             )
    #             SELECT
    #                 {brand_id},
    #                 'SCIM_CONFIG',
    #                 '1',
    #                 '{{"scim_version": "v1", "roles_allowed": ["TeamAdmin", "AccountAdmin", "AIAdmin", "rep", "SuperUser", "user", "Cross-TeamAdmin"], "scim_role_type": "STRING", "scim_label_type": "STRING"}}',
    #                 '{{"SCIM_CONFIG": "enable_scim"}}',
    #                 'ACTIVE',
    #                 NOW(),
    #                 {brand_admin_id},
    #                 NOW(),
    #                 {brand_admin_id},
    #                 NULL,
    #                 NULL
    #             WHERE NOT EXISTS (
    #                 SELECT 1 FROM brands_config WHERE brand_id = {brand_id} AND config_type = 'SCIM_CONFIG'
    #             );
    #
    #         """

    # query_execution(conn_conf_store, config_store_sql, cursor_conf)

    # print("✅ All queries executed successfully. Changes committed.")
    #
    # print(f"📧 Zendesk User Email: {zendesk_user_email}")
    # print(f"👤 Zendesk User Name: {zendesk_user_name}")
    # print(f"Brand Admin: {brand_admin_id}")
    # print(f"Brand ID: {brand_id}")

    return zendesk_user_email, zendesk_user_name, brand_admin_id, brand_id


# def main():
#
#     # brand_name = args.brand_name  # DB ke hisaab se rakhna hai
#
#     zendesk_user_email, zendesk_user_name, brand_admin_id, brand_id = get_variables(brand_name)
#
#     print("✅ All queries executed successfully. Changes committed.")
#
#     print(f"📧 Zendesk User Email: {zendesk_user_email}")
#     print(f"👤 Zendesk User Name: {zendesk_user_name}")
#     print(f"Brand Admin: {brand_admin_id}")
#     print(f"Brand ID: {brand_id}")
#
#
# if __name__ == "__main__":
#     main()




# sql = f"""
    #         SET @brandName := "{brand_name}";
    #
    #         SET @brand_id = (SELECT id FROM brand WHERE name = @brandName);
    #         SET @account_id = (SELECT id FROM account WHERE brandName = @brand_id AND name = @brandName);
    #         SET @BRANDADMIN = (SELECT email FROM user WHERE account_id = @account_id AND firstName LIKE "%Brand%" AND lastName LIKE "%Admin%");
    #         SET @ACCOUNTID = (SELECT id FROM account WHERE name = @brandName);
    #         SET @BRANDID = (SELECT id FROM brand WHERE name = @brandName);
    #         SET @CREATEDBY = (SELECT id FROM user WHERE email = @BRANDADMIN);
    #
    #         select @BRANDID;
    #
    #         select @CREATEDBY;
    #
    #         INSERT INTO `tag_collections` (`name`, `account_id`, `brand_id`, `inactive`, `created_by`, `entity`)
    #         VALUES ('Interruptions', @ACCOUNTID, @BRANDID, 0, @CREATEDBY, 3);
    #
    #         SET @TAGCOLLECTIONID = (SELECT id FROM `tag_collections` WHERE `name` = 'Interruptions' AND account_id = @ACCOUNTID);
    #
    #         INSERT INTO `tags` (`name`, `bg_color`, `account_id`, `brand_id`, `parent_id`, `level`, `inactive`, `tag_collection_id`, `created_by`) VALUES
    #         ('Soft Skills', NULL, @ACCOUNTID , @BRANDID, 0, 1, 0, @TAGCOLLECTIONID, @CREATEDBY),
    #         ('Best Practices', NULL, @ACCOUNTID, @BRANDID, 0, 1, 0, @TAGCOLLECTIONID, @CREATEDBY),
    #         ('Compliance', NULL, @ACCOUNTID, @BRANDID, 0, 1, 0, @TAGCOLLECTIONID, @CREATEDBY);
    #
    #         SET @SOFT_SKILLS = (SELECT id FROM `tags` WHERE `name` = 'Soft Skills' AND account_id = @ACCOUNTID);
    #         SET @BEST_PRACTICES = (SELECT id FROM `tags` WHERE `name` = 'Best Practices' AND account_id = @ACCOUNTID);
    #         SET @COMPLIANCE = (SELECT id FROM `tags` WHERE `name` = 'Compliance' AND account_id = @ACCOUNTID);
    #
    #         INSERT INTO `tags` (`name`, `bg_color`, `account_id`, `brand_id`, `parent_id`, `level`, `inactive`, `tag_collection_id`, `created_by`) VALUES
    #         ('Empathy/Acknowledgement', NULL, @ACCOUNTID, @BRANDID, @SOFT_SKILLS, 2, 0, @TAGCOLLECTIONID, @CREATEDBY),
    #         ('Call Opening', NULL, @ACCOUNTID, @BRANDID, @BEST_PRACTICES, 2, 0, @TAGCOLLECTIONID, @CREATEDBY),
    #         ('Probing Questions', NULL, @ACCOUNTID, @BRANDID, @BEST_PRACTICES, 2, 0, @TAGCOLLECTIONID, @CREATEDBY),
    #         ('Issue Resolution', NULL, @ACCOUNTID, @BRANDID, @BEST_PRACTICES, 2, 0, @TAGCOLLECTIONID, @CREATEDBY),
    #         ('Call Closing', NULL, @ACCOUNTID, @BRANDID, @BEST_PRACTICES, 2, 0, @TAGCOLLECTIONID, @CREATEDBY),
    #         ('Authentication', NULL, @ACCOUNTID, @BRANDID, @COMPLIANCE, 2, 0, @TAGCOLLECTIONID, @CREATEDBY),
    #         ('Disclosures', NULL, @ACCOUNTID, @BRANDID, @COMPLIANCE, 2, 0, @TAGCOLLECTIONID, @CREATEDBY);
    #
    #         SET @brand_url = (SELECT url FROM brand WHERE name = @brandName);
    #         SET @zendesk_user = CONCAT(SUBSTRING_INDEX(@brand_url, '.', 1), '.zendesk@zenarate.com');
    #
    #         INSERT INTO brand_configs (brand_id, config_type, config_json, inactive, created_by, created_at)
    #         VALUES
    #         (@brand_id, 'ZENDESK_CONFIG', CONCAT('{{"enable": true, "zendesk_user_name": "{brand_name}", "zendesk_user_email": "', @zendesk_user, '"}}'), 0, 0, NOW());
    #
    #         INSERT INTO brand_configs (brand_id, config_type, config_json, inactive, created_by, created_at)
    #         VALUES (@brand_id, 'SCIM_CONFIG', '{{"roles_allowed": ["TeamAdmin", "AccountAdmin", "AIAdmin", "rep", "SuperUser", "user", "Cross-TeamAdmin"]}}', 0, 0, NOW());
    #
    #         UPDATE brand_settings
    #         SET settings_json = CONCAT(
    #             LEFT(settings_json, LENGTH(settings_json) - 1),
    #             ', "zendesk_user_name": "{brand_name}", "zendesk_user_email": "', @zendesk_user, '"}}'
    #         )
    #         WHERE brand_id = @BRANDID;
    #
    #         INSERT INTO `story_completion_criteria` (`brand_id`, `story_id`, `criteria_json`)
    #         VALUES
    #         (@brand_id, NULL, '{{"nlp":{{"story_end":{{"_and":[{{"nlp_end":{{"value_type":"bool","opr":"equalsto","value":true}}}},{{"screensim_end":{{"value_type":"bool","opr":"equalsto","value":true}}}}]}}}}}}');
    #
    #         SELECT @zendesk_user AS zendesk_user_email, @brandName AS zendesk_user_name;
    #
    # """

    # config_store_sql = f"""
    #
    #         INSERT INTO brands_config (
    #         brand_id, config_type, enabled, config_json, mapper, status,
    #         created_at, created_by, updated_at, updated_by, deleted_at, deleted_by
    #         )
    #         VALUES
    #         (
    #             {brand_id},
    #             'SCIM_CONFIG',
    #             '1',
    #             '{{"scim_version": "v1", "roles_allowed": ["TeamAdmin", "AccountAdmin", "AIAdmin", "rep", "SuperUser", "user", "Cross-TeamAdmin"], "scim_role_type": "STRING", "scim_label_type": "STRING"}}',
    #             '{{"SCIM_CONFIG": "enable_scim"}}',
    #             'ACTIVE',
    #             NOW(),
    #             {brand_admin_id},
    #             NOW(),
    #             {brand_admin_id},
    #             NULL,
    #             NULL
    #         );
    #
    # """
