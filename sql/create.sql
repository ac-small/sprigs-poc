-- Table: public.flyer_item

-- DROP TABLE public.flyer_item;

CREATE TABLE public.flyer_item
(
    price_units character varying(100) COLLATE pg_catalog."default",
    start_date date,
    sale_price integer,
    product_name character varying(500) COLLATE pg_catalog."default",
    merchant character varying(100) COLLATE pg_catalog."default",
    end_date date,
    id bigint NOT NULL DEFAULT nextval('flyer_item_id_seq'::regclass),
    classification character varying(150) COLLATE pg_catalog."default",
    CONSTRAINT pk_id PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.flyer_item
    OWNER to postgres;