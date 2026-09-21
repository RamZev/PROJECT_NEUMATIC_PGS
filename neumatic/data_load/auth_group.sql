--
-- PostgreSQL database dump
--

\restrict ta8ZJ7wC7y6g261sBLgqSLfPj54Rkil5uKojN5gC5jHTXHdd4DYl44xAyRfSJ6H

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

-- Started on 2026-09-20 23:35:00

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
-- TOC entry 5395 (class 0 OID 16396)
-- Dependencies: 221
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.auth_group VALUES (1, 'Administracion');
INSERT INTO public.auth_group VALUES (3, 'Vendedores');
INSERT INTO public.auth_group VALUES (4, 'Encargado Sucursal');
INSERT INTO public.auth_group VALUES (5, 'Deposito');
INSERT INTO public.auth_group VALUES (6, 'Super');
INSERT INTO public.auth_group VALUES (2, 'Puntos de Ventas');


--
-- TOC entry 5402 (class 0 OID 0)
-- Dependencies: 222
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 6, true);


-- Completed on 2026-09-20 23:35:00

--
-- PostgreSQL database dump complete
--

\unrestrict ta8ZJ7wC7y6g261sBLgqSLfPj54Rkil5uKojN5gC5jHTXHdd4DYl44xAyRfSJ6H

