--
-- PostgreSQL database dump
--

\restrict 4aZWG0fQo3MMQwnxppiDmei53LzULXxAnGvgw5hpdNm0n9kI04wfy1wGB9EamW1

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

-- Started on 2026-08-19 11:08:04

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
-- TOC entry 5393 (class 0 OID 54592)
-- Dependencies: 350
-- Data for Name: usuarios_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.usuarios_user VALUES (3, 'pbkdf2_sha256$870000$VxZxUdecBPWNbdOC2NT0O8$v+2pfRIJfBuYNid3z/yeQoHutMVLMS3kIVEOCaNDC94=', '2025-10-31 21:31:20.829689-05', false, 'juan', 'Juan', '', false, true, '2025-10-30 01:20:56-05', '123@gmail.com', NULL, NULL, 'J', 'Z', NULL, 2, 2, 59);
INSERT INTO public.usuarios_user VALUES (4, 'pbkdf2_sha256$870000$2FjwXmFRoOyPNKXGLMzfB7$ceZt+VBs4p2mZn3Y6il7yrc0KBKgTWy0e99vOYnBRNk=', '2025-10-31 22:47:15.940314-05', false, 'alberto', 'Alberto', 'García', false, true, '2025-10-30 01:25:10-05', 'albertogarcia@gmail.com', NULL, NULL, 'AG', 'Z', NULL, 1, 2, 146);
INSERT INTO public.usuarios_user VALUES (5, 'pbkdf2_sha256$870000$l40YysYnE3ID1ZZIOPsfAj$Aaxjq1481WTHcFDe7lwbOFcCqFVgDv/WmURd/x7EAy0=', '2025-10-31 22:31:58.343834-05', false, 'maria', 'Maria', 'Diaz', false, true, '2025-10-31 21:51:50.381092-05', 'ramosric1410@gmail.com', NULL, NULL, 'MD', 'Z', NULL, 2, 2, NULL);
INSERT INTO public.usuarios_user VALUES (6, 'pbkdf2_sha256$870000$fFAOOQLUxTFUAHVmgZwaS4$t8OAdExznmrFxKq/bH8gChcYoqxkzMrtOJDsdZZqIzM=', '2025-11-02 14:21:57.721893-05', false, 'Federico', 'Federico', 'Camiletti', false, true, '2025-11-01 21:53:35.673835-05', 'fede@ndebona.com', NULL, NULL, 'FC', 'Z', NULL, 1, 1, NULL);
INSERT INTO public.usuarios_user VALUES (7, 'pbkdf2_sha256$870000$o7GYQGdqOXdFTLlh8Xxfh1$/pfISSbe28pBVBAqGH4e5wF7dnLOXBH6KTddMwiirRU=', '2025-12-12 22:55:50.858369-05', false, 'Francisco', 'Francisco', '', false, true, '2025-11-02 13:58:45.399568-05', 'fran@ndebona.com', NULL, NULL, 'FF', 'Z', NULL, 1, 1, NULL);
INSERT INTO public.usuarios_user VALUES (8, 'pbkdf2_sha256$870000$rFndc2IRyHzrNeQdR2yu5S$EGptqcjIPvP58Omzva4wof9QTq4M+1FNLG2u0ug++so=', '2026-04-20 14:08:18.539822-05', false, 'soporte', '', '', false, true, '2026-04-08 15:13:12-05', 'encargado1@ndebona.com.ar', NULL, NULL, NULL, 'Z', NULL, 5, 1, NULL);
INSERT INTO public.usuarios_user VALUES (24, 'pbkdf2_sha256$870000$zepAfHwQFqUmH5xNTGbvOh$3T0wyn6w++Il20AT2Kg2rB16QSedXJxPhLveD5fOie8=', '2026-04-16 15:13:21.566715-05', false, 'marcelo.debona', 'Marcelo', 'Debona', false, true, '2026-04-16 14:57:11.172402-05', 'marcelodebona@ndeona.com.ar', NULL, NULL, 'MD', 'A', NULL, 1, 1, NULL);
INSERT INTO public.usuarios_user VALUES (34, 'pbkdf2_sha256$870000$QZfAh8MzruKwqKcOoK6atQ$WjYf9z3omqIVXEUjMoRUKjZBjUmyy41jeqKf1GUjQzw=', NULL, false, 'alejandro.vargas', 'Alejandro', 'Vargas', false, true, '2026-04-23 13:09:09.503115-05', 'soporte@maasoft.com.ar', NULL, NULL, 'AV', 'Z', NULL, 4, 4, NULL);
INSERT INTO public.usuarios_user VALUES (31, 'pbkdf2_sha256$870000$ffQ5nA4BjQtrKXI3ikXPNN$RbgAuGE45zE7wUML8pj8fCNVyzXmgeqBBelCf66m3hE=', NULL, false, 'mirta.foglia', 'Mirta', 'Foglia', false, true, '2026-04-16 21:03:52.855853-05', 'soporte@maasoft.com.ar', NULL, NULL, 'MF', 'Z', NULL, 1, 1, NULL);
INSERT INTO public.usuarios_user VALUES (21, 'pbkdf2_sha256$870000$vxC7MJCsdHM8dwFAHneriu$Jr9EunY5nWDOFmUbVcuBlCmW+0s7hwgUTfECmcem640=', '2026-07-27 05:40:59.355354-05', false, 'marcelo.paoloni', 'Marcelo', 'Paoloni', false, true, '2026-04-15 16:52:57.913914-05', 'soporte@maasoft.com.ar', NULL, NULL, 'MP', 'Z', NULL, 1, 1, NULL);
INSERT INTO public.usuarios_user VALUES (14, 'pbkdf2_sha256$870000$0ZrvoN4dqpAfG9hhSd4sQT$vBXq4KaOyhHHOyed1XR+tVwhTm1RLSObipwjBXIYdgg=', '2026-07-23 10:04:15.548845-05', false, 'franco.moscatti', 'Franco', 'Moscatti', false, true, '2026-04-14 13:40:11.858039-05', 'soporte@maasoft.com.ar', NULL, NULL, 'FO', 'Z', NULL, 5, 6, NULL);
INSERT INTO public.usuarios_user VALUES (33, 'pbkdf2_sha256$870000$kDFd700gIQfVlgyedC9xtc$7Cr2i9n/lGWOiGi5eIkvR8v+tKm3hW0QcOLUgubpNhM=', '2026-07-14 09:52:36.312715-05', false, 'jonatan.benitez', 'Jonatan', 'Benitez', false, true, '2026-04-22 15:47:59.653028-05', 'soporte@maasoft.com.ar', NULL, NULL, 'JB', 'Z', true, 4, 4, NULL);
INSERT INTO public.usuarios_user VALUES (25, 'pbkdf2_sha256$870000$qVfBPrggPbrt0pW3cc5oKF$elyy5vp/Jd5Gdy0RoPad8EErG7SPAsIjPjmzKfnDiM8=', '2026-07-29 09:42:02.462376-05', false, 'gustavo.cardelino', 'Gustavo', 'Cardelino', false, true, '2026-04-16 20:29:57.881345-05', 'soporte@maasoft.com.ar', NULL, NULL, 'GC', 'Z', NULL, 2, 2, NULL);
INSERT INTO public.usuarios_user VALUES (28, 'pbkdf2_sha256$870000$6DH21UGU5RByPq8qsnJykv$KDwVs7e3OzviyE8vzixSN5VvUu3G+cVFbs4CEBmDDS4=', '2026-07-30 06:23:18.234891-05', false, 'jose.geambeau', 'Jose', 'Geambeau', false, true, '2026-04-16 20:37:02.298743-05', 'soporte@maasoft.com.ar', NULL, NULL, 'JG', 'Z', NULL, 6, 7, NULL);
INSERT INTO public.usuarios_user VALUES (35, 'pbkdf2_sha256$870000$ajahq4a9P7PVie2qNctEJ9$A0imM8557OpZt+p9/B0kqTHs4X/MtfZSbqcO9Xowg0E=', '2026-07-23 15:30:04.756109-05', false, 'carla.baroni', 'Carla', 'Baroni', false, true, '2026-04-24 13:39:41.108073-05', 'soporte@maasoft.com.ar', NULL, NULL, 'CB', 'Z', true, 1, 1, NULL);
INSERT INTO public.usuarios_user VALUES (17, 'pbkdf2_sha256$870000$rNu5jdDlQqo8MPrmKEo1Op$RhCGyWPDl7qYmcbKXd0l76IzZy6pFPfo3TxVTw18vnM=', '2026-07-30 06:48:59.666372-05', false, 'francisco.strada', 'Francisco', 'Strada', false, true, '2026-04-14 13:42:33.505903-05', 'soporte@maasoft.com.ar', NULL, NULL, 'FE', 'Z', NULL, 1, 1, NULL);
INSERT INTO public.usuarios_user VALUES (20, 'pbkdf2_sha256$870000$xQElZUBGHFK7ZR3oLCKZHA$u2bxQVhM4fqAk6/ox08ETbPNXGEahGODYpYiuKRJytw=', '2026-07-21 06:07:25.365323-05', false, 'yemel.gazze', 'Yemel', 'Gazze', false, true, '2026-04-15 15:25:59.756744-05', 'soporte@maasoft.com.ar', NULL, NULL, 'YG', 'Z', NULL, 7, 8, NULL);
INSERT INTO public.usuarios_user VALUES (18, 'pbkdf2_sha256$870000$wJ4V5uoEWwXdFB1pKYB03S$NLhLPGCljh/dbjEZqRuJRdxP9ghENIjrcOs60Rk9lug=', '2026-07-28 12:42:54.923-05', false, 'luciano.cerutti', 'Luciano', 'Cerutti', false, true, '2026-04-14 15:28:21.694699-05', 'soporte@maasoft.com.ar', NULL, NULL, 'LC', 'Z', NULL, 9, 10, NULL);
INSERT INTO public.usuarios_user VALUES (16, 'pbkdf2_sha256$870000$BrAUxnOuk77jfBryt3mPkt$NwqA2ijpRpGq5Ow1AehXsVgfkeSU1AgWbG8RMmRbz9Q=', '2026-07-21 08:04:45.616868-05', false, 'ivan.alemany', 'Ivan', 'Alemany', false, true, '2026-04-14 13:41:41.60578-05', 'soporte@maasoft.com.ar', NULL, NULL, 'IA', 'Z', NULL, 7, 8, NULL);
INSERT INTO public.usuarios_user VALUES (11, 'pbkdf2_sha256$870000$zl0DDjWL3zr5HjOy2fGZ8d$hYTQ95erANXtjNBd8z0q8EvC+Cu0r1hMxD2wjRZgUvg=', '2026-07-30 06:40:55.906194-05', false, 'ramon.mendez', 'Ramon', 'Mendez', false, true, '2026-04-14 13:36:17.167374-05', 'soporte@maasoft.com.ar', NULL, NULL, 'RM', 'Z', NULL, 6, 7, NULL);
INSERT INTO public.usuarios_user VALUES (10, 'pbkdf2_sha256$870000$18DFCZePWuZG69V4xMP079$qPHm70BnjOW38NuhhJBbXl5aMaQNKENvQMBb/JEn3io=', '2026-07-27 07:48:50.237927-05', false, 'federico.camilletti', 'Federico', 'Camilletti', false, true, '2026-04-14 13:35:36.004415-05', 'soporte@maasoft.com.ar', NULL, NULL, 'FC', 'Z', NULL, 1, 1, NULL);
INSERT INTO public.usuarios_user VALUES (22, 'pbkdf2_sha256$870000$C38wtwaEnCPZ3N6rfjbXes$mK/9WQd/0vyRTQare4WHrnL/vTknZiSFIkWweI5fnwM=', '2026-07-28 10:11:21.106967-05', false, 'cesar.keller', 'Cesar', 'Keller', false, true, '2026-04-15 19:19:06.697582-05', 'soporte@maasoft.com.ar', NULL, NULL, 'CK', 'Z', NULL, 9, 10, NULL);
INSERT INTO public.usuarios_user VALUES (19, 'pbkdf2_sha256$870000$M3uQWGLp2jLDfhe9e9ieLE$+wDwNgcmwC46GurhDjgPTFWndDC6kMO7TltXAfrR250=', '2026-07-27 08:57:16.421923-05', false, 'lucas.debona', 'Lucas', 'Debona', false, true, '2026-04-15 15:25:11.129646-05', 'soporte@maasoft.com.ar', NULL, NULL, 'LD', 'Z', NULL, 3, 3, NULL);
INSERT INTO public.usuarios_user VALUES (27, 'pbkdf2_sha256$870000$RH5APpPozFoHNfcRIBLfAy$+e4Q9LpzJ5kyjIDmKNqg3j2EX7gwRhGAgxVCMxuDanQ=', '2026-07-29 10:05:48.757928-05', false, 'cesar.bordessolles', 'Cesar', 'Bordessolles', false, true, '2026-04-16 20:32:18.700039-05', 'soporte@maasoft.com.ar', NULL, NULL, 'CE', 'Z', NULL, 2, 2, NULL);
INSERT INTO public.usuarios_user VALUES (15, 'pbkdf2_sha256$870000$FbhPbtVAo80nlpfiqQpEZ8$18hXh2yHjFNIrby+mJeqEMpaerdOJOKnexAfHgOJ+40=', '2026-07-28 06:37:38.632962-05', false, 'david.ortiz', 'David', 'Ortiz', false, true, '2026-04-14 13:41:07.565852-05', 'soporte@maasoft.com.ar', NULL, NULL, 'DV', 'Z', NULL, 3, 3, NULL);
INSERT INTO public.usuarios_user VALUES (32, 'pbkdf2_sha256$870000$G7ftcK7UUebpqoJ4Cwvypr$wrKsEDKGtATjASGwneAYce1H9YbnqvR89DrBPeXLHLw=', '2026-07-28 07:01:46.998403-05', false, 'javier.schechtel', 'Javier', 'Schechtel', false, true, '2026-04-17 12:57:45.044818-05', 'soporte@maasoft.com.ar', NULL, NULL, 'JS', 'Z', NULL, 3, 3, NULL);
INSERT INTO public.usuarios_user VALUES (9, 'pbkdf2_sha256$870000$5Ogd0hL034f8kRStKPNsyZ$rAunufs164KVVAPF6TQLQdT5yXQtuxXW4nbqO3dIGHw=', '2026-07-29 11:14:01.676053-05', false, 'leandro.milessi', 'Leandro', 'Milessi', false, true, '2026-04-14 13:32:54.58771-05', 'soporte@maasoft.com.ar', NULL, NULL, 'LE', 'Z', NULL, 9, 10, NULL);
INSERT INTO public.usuarios_user VALUES (26, 'pbkdf2_sha256$870000$C4E8Wexzdc00bzsh5wcMZE$2L53F0fvp8B4EcDPqTbJGUtE/cNH1b8I6+erl2/IRwY=', '2026-07-29 06:04:36.849873-05', false, 'eliana.bosco', 'Eliana', 'Bosco', false, true, '2026-04-16 20:30:52.687152-05', 'soporte@maasoft.com.ar', NULL, NULL, 'EB', 'Z', NULL, 2, 2, NULL);
INSERT INTO public.usuarios_user VALUES (12, 'pbkdf2_sha256$870000$3ytkQZkT3ob4MydDYZIxwg$XeEiSOBdw1mxJKsjqSVP6ynpUeGYeAaXshhcAmxDPmU=', '2026-07-28 14:25:38.712022-05', false, 'pablo.romero', 'Pablo', 'Romero', false, true, '2026-04-14 13:36:50.338411-05', 'soporte@maasoft.com.ar', NULL, NULL, 'PR', 'Z', true, 4, 4, NULL);
INSERT INTO public.usuarios_user VALUES (30, 'pbkdf2_sha256$870000$DzK65bLgHg1JCgrNKVQB2o$RSQpBi7Yaqoe1cYmytRb0rVTlsBz0mcw2ZB3pgxJc2E=', '2026-07-29 06:07:42.831121-05', false, 'axel.zalazar', 'Axel', 'Zalazar', false, true, '2026-04-16 20:40:34.208579-05', 'soporte@maasoft.com.ar', NULL, NULL, 'AZ', 'Z', NULL, 2, 2, NULL);
INSERT INTO public.usuarios_user VALUES (23, 'pbkdf2_sha256$870000$lYJ3h8IJE2S4jGQedFCoF3$Kx6FqiLvWLqCeTCQFLKUIulV9nb0pMLQ1mcNi8SkTfo=', '2026-07-30 07:25:15.885327-05', false, 'gonzalo.bustos', 'Gonzalo', 'Bustos', false, true, '2026-04-15 19:39:31.416751-05', 'soporte@maasoft.com.ar', NULL, NULL, 'GB', 'Z', true, 12, 12, NULL);
INSERT INTO public.usuarios_user VALUES (13, 'pbkdf2_sha256$870000$BVQXCuS4XTewrjG4ovfmkx$l6oPdzjpsmlimzv92Otwc80ABlSLNPrWPP19dq7F93o=', '2026-07-30 13:29:53.793344-05', false, 'fabiana.verrino', 'Fabiana', 'Verrino', false, true, '2026-04-14 13:39:38.735284-05', 'soporte@maasoft.com.ar', NULL, NULL, 'FV', 'Z', true, 12, 12, NULL);
INSERT INTO public.usuarios_user VALUES (36, 'pbkdf2_sha256$870000$2Nd59kxY60WaUJOWoi2XEP$FnsZh16Nrt2Czk7T/7udOytJoh0ij9Oj1uzzeBcmc7s=', '2026-07-30 09:41:34.177409-05', false, 'alejandro.barbero', 'Alejandro', 'Barbero', false, true, '2026-04-27 15:13:57.08095-05', 'soporte@maasoft.com.ar', NULL, NULL, 'AB', 'Z', true, 10, 11, NULL);
INSERT INTO public.usuarios_user VALUES (29, 'pbkdf2_sha256$870000$zeZgRL1INFvYJvRGFRyqYK$d8t3H6BeHWa83MbwSSFBSMA5yiCGSt3amU8qIf11APY=', '2026-07-14 07:16:35.054634-05', false, 'mariano.saldarini', 'Mariano', 'Saldarini', false, true, '2026-04-16 20:38:24.795782-05', 'soporte@maasoft.com.ar', NULL, NULL, 'MS', 'Z', NULL, 4, 4, NULL);
INSERT INTO public.usuarios_user VALUES (37, 'pbkdf2_sha256$870000$MWpbL4pK5hPEdhJ22JFyiU$PH1cDDpxaMaR82Hch8MbicpLKw/reqPMCw/8mneB9R8=', '2026-07-27 08:31:20.38746-05', false, 'fernando.godoy', 'Fernando', 'Godoy', false, true, '2026-07-02 08:54:02.532856-05', 'soporte@maasoft.com.ar', NULL, NULL, NULL, 'Z', false, 4, 4, NULL);
INSERT INTO public.usuarios_user VALUES (38, 'pbkdf2_sha256$870000$Qwbzb77G6VkxcVNwbqmVxF$nGuLkj6852aGPbJbJ2H4vSbiGsbWl4QvPUkfGqyFpy0=', NULL, false, 'emiliano.flores', 'Emiliano', 'Flores', false, true, '2026-07-28 15:06:39.575493-05', 'soporte@maasoft.com.ar', NULL, NULL, 'EF', 'Z', true, 9, 10, NULL);
INSERT INTO public.usuarios_user VALUES (39, 'pbkdf2_sha256$870000$QEaTbeTDNxrIPOD521u7xJ$LoQM0SinsFwSxnvHCYtotudH2t1lOQrqFEVN7cjTK2E=', NULL, false, 'sebastian.long', '', '', false, true, '2026-07-30 10:16:06.50615-05', 'soporte@maasoft.com.ar', NULL, NULL, NULL, 'Z', true, 6, 7, NULL);
INSERT INTO public.usuarios_user VALUES (1, 'pbkdf2_sha256$870000$gZCJD8Qg3sa512uO9LGM3Y$e4Hlcvo8Gh9J3WaLR+9lxicIiTTtyWuony1lXn0XVW4=', '2026-08-17 19:34:11.635708-05', true, 'admin', '', '', true, true, '2026-08-02 19:58:56.672301-05', 'ramosric1410@gmail.com', NULL, NULL, NULL, 'Z', false, 2, 2, 1);


--
-- TOC entry 5400 (class 0 OID 0)
-- Dependencies: 353
-- Name: usuarios_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarios_user_id_seq', 1, true);


-- Completed on 2026-08-19 11:08:04

--
-- PostgreSQL database dump complete
--

\unrestrict 4aZWG0fQo3MMQwnxppiDmei53LzULXxAnGvgw5hpdNm0n9kI04wfy1wGB9EamW1

