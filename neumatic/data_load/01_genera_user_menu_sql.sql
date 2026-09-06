COPY (
    -- auth_group
    SELECT 'INSERT INTO public.auth_group VALUES (' || id || ', ' || quote_literal(name) || ');'
    FROM auth_group
    UNION ALL
    -- auth_group_permissions
    SELECT 'INSERT INTO public.auth_group_permissions VALUES (' || id || ', ' || group_id || ', ' || permission_id || ');'
    FROM auth_group_permissions
    UNION ALL
    -- usuarios_user (excluye admin)
    SELECT 'INSERT INTO public.usuarios_user VALUES (' || 
           id || ', ' || 
           quote_literal(password) || ', ' || 
           COALESCE(quote_literal(last_login::text), 'NULL') || ', ' || 
           CASE WHEN is_superuser THEN 'TRUE' ELSE 'FALSE' END || ', ' || 
           quote_literal(username) || ', ' || 
           quote_literal(first_name) || ', ' || 
           quote_literal(last_name) || ', ' || 
           CASE WHEN is_staff THEN 'TRUE' ELSE 'FALSE' END || ', ' || 
           CASE WHEN is_active THEN 'TRUE' ELSE 'FALSE' END || ', ' || 
           quote_literal(date_joined::text) || ', ' || 
           quote_literal(email) || ', ' || 
           COALESCE(quote_literal(email_alt), 'NULL') || ', ' || 
           COALESCE(quote_literal(telefono), 'NULL') || ', ' || 
           COALESCE(quote_literal(iniciales), 'NULL') || ', ' || 
           COALESCE(quote_literal(jerarquia), 'NULL') || ', ' || 
           COALESCE(CASE WHEN cambia_precio_descripcion THEN 'TRUE' ELSE 'FALSE' END, 'NULL') || ', ' || 
           COALESCE(id_punto_venta_id::text, 'NULL') || ', ' || 
           COALESCE(id_sucursal_id::text, 'NULL') || ', ' || 
           COALESCE(id_vendedor_id::text, 'NULL') || ');'
    FROM usuarios_user
    WHERE username != 'admin'
    UNION ALL
    -- usuarios_user_groups
    SELECT 'INSERT INTO public.usuarios_user_groups VALUES (' || id || ', ' || user_id || ', ' || group_id || ');'
    FROM usuarios_user_groups
    UNION ALL
    -- menu_menuheading
    SELECT 'INSERT INTO public.menu_menuheading VALUES (' || 
           id_menu_heading || ', ' || 
           quote_literal(name) || ', ' || 
           "order" || ');'
    FROM menu_menuheading
    UNION ALL
    -- menu_menuitem
    SELECT 'INSERT INTO public.menu_menuitem VALUES (' || 
           id_menu_item || ', ' || 
           quote_literal(name) || ', ' || 
           quote_literal(url_name) || ', ' || 
           quote_literal(query_params) || ', ' || 
           COALESCE(quote_literal(icon), 'NULL') || ', ' || 
           CASE WHEN is_collapse THEN 'TRUE' ELSE 'FALSE' END || ', ' || 
           "order" || ', ' || 
           COALESCE(orden_acceso_directo::text, 'NULL') || ', ' || 
           COALESCE(heading_id::text, 'NULL') || ', ' || 
           COALESCE(parent_id::text, 'NULL') || ');'
    FROM menu_menuitem
    UNION ALL
    -- menu_menuitem_groups
    SELECT 'INSERT INTO public.menu_menuitem_groups VALUES (' || id || ', ' || menuitem_id || ', ' || group_id || ');'
    FROM menu_menuitem_groups
) TO 'D:/NEUMATIC_BAK/sql_user_menu/user_menu.sql';