--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1
-- Dumped by pg_dump version 13.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


--
-- Name: id_sequence; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.id_sequence
    START WITH 2
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.id_sequence OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: raven_summarybyquarter; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.raven_summarybyquarter (
    saleqty double precision,
    salevalue money,
    inventoryqty double precision,
    inventoryvalue money
);


ALTER TABLE public.raven_summarybyquarter OWNER TO postgres;

--
-- Data for Name: raven_summarybyquarter; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.raven_summarybyquarter (saleqty, salevalue, inventoryqty, inventoryvalue) FROM stdin;
2698	Rp355.834.198,00	5078	Rp827.713.819,00
\.


--
-- Name: id_sequence; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.id_sequence', 4, true);


--
-- PostgreSQL database dump complete
--

