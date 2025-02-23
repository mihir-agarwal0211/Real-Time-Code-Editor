--
-- PostgreSQL database dump
--

-- Dumped from database version 17.3
-- Dumped by pg_dump version 17.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
-- SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public;
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: code_files; Type: TABLE; Schema: public;
--

CREATE TABLE public.code_files (
    id character varying NOT NULL,
    name character varying NOT NULL,
    content text,
    owner_id character varying
);

--
-- Name: editing_sessions; Type: TABLE; Schema: public;
--

CREATE TABLE public.editing_sessions (
    id character varying NOT NULL,
    file_id character varying,
    user_id character varying,
    cursor_position text,
    last_updated timestamp without time zone
);

--
-- Name: users; Type: TABLE; Schema: public;
--

CREATE TABLE public.users (
    id character varying NOT NULL,
    username character varying NOT NULL,
    password_hash character varying NOT NULL,
    role character varying
);

--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public;
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: code_files code_files_pkey; Type: CONSTRAINT; Schema: public;
--

ALTER TABLE ONLY public.code_files
    ADD CONSTRAINT code_files_pkey PRIMARY KEY (id);


--
-- Name: editing_sessions editing_sessions_pkey; Type: CONSTRAINT; Schema: public;
--

ALTER TABLE ONLY public.editing_sessions
    ADD CONSTRAINT editing_sessions_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public;
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public;
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: ix_code_files_id; Type: INDEX; Schema: public;
--

CREATE INDEX ix_code_files_id ON public.code_files USING btree (id);


--
-- Name: ix_editing_sessions_id; Type: INDEX; Schema: public;
--

CREATE INDEX ix_editing_sessions_id ON public.editing_sessions USING btree (id);


--
-- Name: ix_users_id; Type: INDEX; Schema: public;
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: code_files code_files_owner_id_fkey; Type: FK CONSTRAINT; Schema: public;
--

ALTER TABLE ONLY public.code_files
    ADD CONSTRAINT code_files_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(id);


--
-- Name: editing_sessions editing_sessions_file_id_fkey; Type: FK CONSTRAINT; Schema: public;
--

ALTER TABLE ONLY public.editing_sessions
    ADD CONSTRAINT editing_sessions_file_id_fkey FOREIGN KEY (file_id) REFERENCES public.code_files(id);


--
-- Name: editing_sessions editing_sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public;
--

ALTER TABLE ONLY public.editing_sessions
    ADD CONSTRAINT editing_sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

