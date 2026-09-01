--
-- PostgreSQL database dump
--

\restrict BgrYfnHSihde1dRw8b4G3xGN1hDaepp9NGF7UM0LRhwTYMLAIK2glB7kXAs6IGN

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

-- Started on 2026-09-01 00:37:52

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
-- TOC entry 5390 (class 0 OID 59668)
-- Dependencies: 351
-- Data for Name: usuarios_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.usuarios_user_groups VALUES (1, 3, 2);
INSERT INTO public.usuarios_user_groups VALUES (2, 4, 1);
INSERT INTO public.usuarios_user_groups VALUES (3, 5, 3);
INSERT INTO public.usuarios_user_groups VALUES (4, 6, 4);
INSERT INTO public.usuarios_user_groups VALUES (5, 7, 2);
INSERT INTO public.usuarios_user_groups VALUES (7, 9, 4);
INSERT INTO public.usuarios_user_groups VALUES (8, 10, 4);
INSERT INTO public.usuarios_user_groups VALUES (9, 11, 4);
INSERT INTO public.usuarios_user_groups VALUES (10, 12, 4);
INSERT INTO public.usuarios_user_groups VALUES (11, 13, 4);
INSERT INTO public.usuarios_user_groups VALUES (12, 14, 4);
INSERT INTO public.usuarios_user_groups VALUES (13, 16, 4);
INSERT INTO public.usuarios_user_groups VALUES (14, 17, 2);
INSERT INTO public.usuarios_user_groups VALUES (16, 18, 4);
INSERT INTO public.usuarios_user_groups VALUES (19, 20, 2);
INSERT INTO public.usuarios_user_groups VALUES (20, 21, 5);
INSERT INTO public.usuarios_user_groups VALUES (22, 23, 2);
INSERT INTO public.usuarios_user_groups VALUES (25, 15, 2);
INSERT INTO public.usuarios_user_groups VALUES (26, 8, 2);
INSERT INTO public.usuarios_user_groups VALUES (28, 24, 6);
INSERT INTO public.usuarios_user_groups VALUES (29, 19, 1);
INSERT INTO public.usuarios_user_groups VALUES (30, 25, 2);
INSERT INTO public.usuarios_user_groups VALUES (31, 26, 2);
INSERT INTO public.usuarios_user_groups VALUES (32, 27, 2);
INSERT INTO public.usuarios_user_groups VALUES (33, 28, 2);
INSERT INTO public.usuarios_user_groups VALUES (34, 29, 2);
INSERT INTO public.usuarios_user_groups VALUES (35, 30, 2);
INSERT INTO public.usuarios_user_groups VALUES (36, 33, 2);
INSERT INTO public.usuarios_user_groups VALUES (37, 34, 5);
INSERT INTO public.usuarios_user_groups VALUES (38, 35, 1);
INSERT INTO public.usuarios_user_groups VALUES (39, 31, 1);
INSERT INTO public.usuarios_user_groups VALUES (41, 32, 5);
INSERT INTO public.usuarios_user_groups VALUES (43, 37, 1);
INSERT INTO public.usuarios_user_groups VALUES (44, 1, 6);
INSERT INTO public.usuarios_user_groups VALUES (45, 38, 5);
INSERT INTO public.usuarios_user_groups VALUES (46, 36, 4);
INSERT INTO public.usuarios_user_groups VALUES (6, 2, 2);
INSERT INTO public.usuarios_user_groups VALUES (15, 22, 5);


--
-- TOC entry 5397 (class 0 OID 0)
-- Dependencies: 352
-- Name: usuarios_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarios_user_groups_id_seq', 15, true);


-- Completed on 2026-09-01 00:37:52

--
-- PostgreSQL database dump complete
--

\unrestrict BgrYfnHSihde1dRw8b4G3xGN1hDaepp9NGF7UM0LRhwTYMLAIK2glB7kXAs6IGN

