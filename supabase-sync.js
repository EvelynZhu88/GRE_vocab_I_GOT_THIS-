/* GRE Vocab — Supabase sync layer
 *
 * Stores per-user app state (progress, units, settings) in a single row
 * of the user_state table, keyed by auth.uid(). Last-write-wins.
 *
 * Setup:
 *   1) Create a Supabase project at https://supabase.com
 *   2) In the SQL editor, run the SQL block from README / setup notes
 *      (creates the user_state table, RLS policies, and updated_at trigger)
 *   3) In Authentication > URL Configuration, add your site URL to
 *      "Site URL" and to "Additional Redirect URLs" — e.g.
 *        https://evelynzhu88.github.io/GRE_vocab_I_GOT_THIS-/
 *        http://localhost:8000  (for local testing)
 *   4) Paste your project URL + anon key below.
 *
 * The anon key is PUBLIC by design — Row-Level Security in the database
 * is what actually protects data. Safe to commit.
 */
const SUPABASE_URL  = 'https://mibcrghrwxsyknbmdzpm.supabase.co';   // e.g. https://abcd1234.supabase.co
const SUPABASE_ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1pYmNyZ2hyd3hzeWtuYm1kenBtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk5MzcyMDAsImV4cCI6MjA5NTUxMzIwMH0.EcC3O5ghLwzZzLSvSMxos15zVpLbhK7N4tYumLpqHc8'; // long eyJ... string

const LOCAL_TS_KEY = 'gre.localUpdatedAt';

let supa = null;
let pushTimer = null;
let lastSyncedAt = 0;
let isPushing = false;

function isConfigured() {
  return (
    typeof window !== 'undefined' &&
    !!window.supabase &&
    typeof SUPABASE_URL === 'string' &&
    SUPABASE_URL.startsWith('https://') &&
    !SUPABASE_URL.startsWith('PASTE_') &&
    typeof SUPABASE_ANON === 'string' &&
    SUPABASE_ANON.length > 20 &&
    !SUPABASE_ANON.startsWith('PASTE_')
  );
}

function client() {
  if (supa) return supa;
  if (!isConfigured()) return null;
  supa = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON, {
    auth: {
      persistSession: true,
      autoRefreshToken: true,
      detectSessionInUrl: true,
      flowType: 'pkce',
    },
  });
  return supa;
}

async function currentUser() {
  const c = client(); if (!c) return null;
  try {
    const { data: { user } } = await c.auth.getUser();
    return user || null;
  } catch { return null; }
}

async function signInWithEmail(email) {
  const c = client(); if (!c) throw new Error('Supabase not configured');
  const redirect = window.location.origin + window.location.pathname;
  const { error } = await c.auth.signInWithOtp({
    email,
    options: { emailRedirectTo: redirect },
  });
  if (error) throw error;
}

async function signOut() {
  const c = client(); if (!c) return;
  await c.auth.signOut();
  lastSyncedAt = 0;
}

// Returns { progress, units, settings, updated_at } or null
async function pullState() {
  const c = client(); if (!c) return null;
  const user = await currentUser();
  if (!user) return null;
  const { data, error } = await c
    .from('user_state')
    .select('progress, units, settings, updated_at')
    .eq('user_id', user.id)
    .maybeSingle();
  if (error) { console.warn('[supa pull]', error); return null; }
  return data;
}

// Debounced push of current state to the server. Caller passes a snapshot.
function schedulePush(state, delay = 1500) {
  clearTimeout(pushTimer);
  pushTimer = setTimeout(() => pushNow(state), delay);
}

async function pushNow(state) {
  const c = client(); if (!c) return;
  if (isPushing) return; // a previous push is in flight; the next save will retrigger
  const user = await currentUser();
  if (!user) return;
  isPushing = true;
  try {
    const { error } = await c.from('user_state').upsert({
      user_id: user.id,
      progress: state.progress || {},
      units: state.units || {},
      settings: state.settings || {},
    }, { onConflict: 'user_id' });
    if (error) console.warn('[supa push]', error);
    else lastSyncedAt = Date.now();
  } catch (e) {
    console.warn('[supa push]', e);
  } finally {
    isPushing = false;
  }
}

function onAuthChange(cb) {
  const c = client(); if (!c) return () => {};
  const { data: sub } = c.auth.onAuthStateChange((_event, session) => {
    cb(session?.user || null);
  });
  return () => sub.subscription.unsubscribe();
}

window.SupaSync = {
  isConfigured,
  currentUser,
  signInWithEmail,
  signOut,
  pullState,
  schedulePush,
  pushNow,
  onAuthChange,
  lastSyncedAt: () => lastSyncedAt,
  LOCAL_TS_KEY,
};
