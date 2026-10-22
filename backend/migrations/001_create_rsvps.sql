-- Creates the RSVP table. Run once in the Supabase SQL Editor (safe to run again).

create table if not exists public.rsvps (
    id               uuid primary key,
    guest_name       varchar(80)  not null,
    phone            varchar(20),
    attendance       varchar(16)  not null,
    guest_count      integer      not null,
    message          varchar(300),
    edit_token_hash  varchar(64)  not null,
    created_at       timestamptz  not null,
    updated_at       timestamptz  not null
);

create index if not exists ix_rsvps_attendance on public.rsvps (attendance);
create index if not exists ix_rsvps_created_at on public.rsvps (created_at);

-- Supabase exposes tables in the public schema through its Data API.
-- Turning on Row Level Security with no policies blocks that API (anon and
-- authenticated keys get nothing). The FastAPI backend connects as the
-- postgres user, which is not affected, so RSVPs stay reachable only through it.
alter table public.rsvps enable row level security;
