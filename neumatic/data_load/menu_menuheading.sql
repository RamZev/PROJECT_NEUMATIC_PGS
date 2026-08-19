--
-- PostgreSQL database dump
--

\restrict nFH2vEPerWjPY707VdhuognObytFsTkuRiP0k7Ax8b80BjAUbuGK1qK2b3UEMyA

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

-- Started on 2026-08-19 11:09:08

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 5384 (class 0 OID 54333)
-- Dependencies: 292
-- Data for Name: menu_menuheading; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.menu_menuheading VALUES (1, 'Archivos', 0);
INSERT INTO public.menu_menuheading VALUES (2, 'Ventas', 1);
INSERT INTO public.menu_menuheading VALUES (3, 'Compras', 3);
INSERT INTO public.menu_menuheading VALUES (4, 'Informes', 2);
INSERT INTO public.menu_menuheading VALUES (6, 'Estadísticas Ventas', 6);
INSERT INTO public.menu_menuheading VALUES (8, 'Tablas Dinamicas', 7);
INSERT INTO public.menu_menuheading VALUES (9, 'Caja', 5);
INSERT INTO public.menu_menuheading VALUES (10, 'Mantenimiento', 9);
INSERT INTO public.menu_menuheading VALUES (11, 'Consultas', 8);
INSERT INTO public.menu_menuheading VALUES (7, 'Configurar menú', 10);


--
-- TOC entry 5391 (class 0 OID 0)
-- Dependencies: 293
-- Name: menu_menuheading_id_menu_heading_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.menu_menuheading_id_menu_heading_seq', 11, true);


-- Completed on 2026-08-19 11:09:08

--
-- PostgreSQL database dump complete
--

\unrestrict nFH2vEPerWjPY707VdhuognObytFsTkuRiP0k7Ax8b80BjAUbuGK1qK2b3UEMyA

