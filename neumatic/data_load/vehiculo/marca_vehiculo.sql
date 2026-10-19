--
-- PostgreSQL database dump
--

\restrict bwjLN0Op50lVNOGaqVqLin2VT18w4wfqK69uNanULfqKY4QbuMaEWzvjBrCmmhd

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

-- Started on 2026-10-15 06:15:27

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
-- TOC entry 5428 (class 0 OID 27055)
-- Dependencies: 420
-- Data for Name: marca_vehiculo; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.430932-05', '2026-10-07 01:09:35.430932-05', 1, true, 'ALFA ROMEO', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.430932-05', '2026-10-07 01:09:35.430932-05', 2, true, 'AUDI', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.430932-05', '2026-10-07 01:09:35.430932-05', 3, true, 'BMW', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.430932-05', '2026-10-07 01:09:35.430932-05', 4, true, 'CHEVROLET', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.430932-05', '2026-10-07 01:09:35.430932-05', 5, true, 'CHERY', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.430932-05', '2026-10-07 01:09:35.430932-05', 6, true, 'CHRYSLER', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.430932-05', '2026-10-07 01:09:35.430932-05', 7, true, 'CITROEN', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.430932-05', '2026-10-07 01:09:35.430932-05', 8, true, 'DAEWOO', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.430932-05', '2026-10-07 01:09:35.430932-05', 9, true, 'DAIHATSU', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.430932-05', '2026-10-07 01:09:35.430932-05', 10, true, 'DODGE', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.430932-05', '2026-10-07 01:09:35.430932-05', 11, true, 'FIAT', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.430932-05', '2026-10-07 01:09:35.430932-05', 12, true, 'FORD', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.430932-05', '2026-10-07 01:09:35.430932-05', 13, true, 'HONDA', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.430932-05', '2026-10-07 01:09:35.430932-05', 14, true, 'HYUNDAI', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.430932-05', '2026-10-07 01:09:35.430932-05', 15, true, 'ISUZU', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.430932-05', '2026-10-07 01:09:35.430932-05', 16, true, 'IVECO', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.430932-05', '2026-10-07 01:09:35.430932-05', 17, true, 'JEEP', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.430932-05', '2026-10-07 01:09:35.430932-05', 18, true, 'KIA', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.430932-05', '2026-10-07 01:09:35.430932-05', 19, true, 'LAND ROVER', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.430932-05', '2026-10-07 01:09:35.430932-05', 20, true, 'MAZDA', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.430932-05', '2026-10-07 01:09:35.430932-05', 21, true, 'MERCEDES BENZ', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.431932-05', '2026-10-07 01:09:35.431932-05', 22, true, 'MERCURY', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.431932-05', '2026-10-07 01:09:35.431932-05', 23, true, 'MINI', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.431932-05', '2026-10-07 01:09:35.431932-05', 24, true, 'MITSUBISHI', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.431932-05', '2026-10-07 01:09:35.431932-05', 25, true, 'NISSAN', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.431932-05', '2026-10-07 01:09:35.431932-05', 26, true, 'OLTCIT', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.431932-05', '2026-10-07 01:09:35.431932-05', 27, true, 'OPEL', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.431932-05', '2026-10-07 01:09:35.431932-05', 28, true, 'PEUGEOT', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.431932-05', '2026-10-07 01:09:35.431932-05', 29, true, 'RENAULT', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.431932-05', '2026-10-07 01:09:35.431932-05', 30, true, 'ROVER', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.431932-05', '2026-10-07 01:09:35.431932-05', 31, true, 'SAAB', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.431932-05', '2026-10-07 01:09:35.431932-05', 32, true, 'SEAT', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.431932-05', '2026-10-07 01:09:35.431932-05', 33, true, 'SSANG YONG', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.431932-05', '2026-10-07 01:09:35.431932-05', 34, true, 'SUBARU', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.431932-05', '2026-10-07 01:09:35.431932-05', 35, true, 'SUZUKI', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.431932-05', '2026-10-07 01:09:35.431932-05', 36, true, 'TOYOTA', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.431932-05', '2026-10-07 01:09:35.431932-05', 37, true, 'VOLKSWAGEN', 1, NULL);
INSERT INTO public.marca_vehiculo VALUES (NULL, NULL, '2026-10-07 01:09:35.431932-05', '2026-10-07 01:09:35.431932-05', 38, true, 'VOLVO', 1, NULL);


--
-- TOC entry 5434 (class 0 OID 0)
-- Dependencies: 419
-- Name: marca_vehiculo_id_marca_vehiculo_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marca_vehiculo_id_marca_vehiculo_seq', 1, false);


-- Completed on 2026-10-15 06:15:28

--
-- PostgreSQL database dump complete
--

\unrestrict bwjLN0Op50lVNOGaqVqLin2VT18w4wfqK69uNanULfqKY4QbuMaEWzvjBrCmmhd

