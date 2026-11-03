"""Converte i GTFS ACTV (bus e navigazione) nel file data.json usato dall'app.
Uso: python3 scripts/build_data.py actv_aut.zip actv_nav.zip data.json"""
import csv, io, json, re, sys, zipfile, collections

def convert(path):
    z = zipfile.ZipFile(path)
    def rows(name):
        if name not in z.namelist():
            return []
        return csv.DictReader(io.TextIOWrapper(z.open(name), encoding='utf-8-sig'))
    stop_name = {r['stop_id']: r['stop_name'].strip() for r in rows('stops.txt')}
    route = {}
    for r in rows('routes.txt'):
        col = r.get('route_color', '')
        route[r['route_id']] = (r['route_short_name'] or r['route_long_name'], '#' + col if len(col) == 6 else '#0a96e0')
    trip = {r['trip_id']: r for r in rows('trips.txt')}
    times = collections.defaultdict(list)
    for r in rows('stop_times.txt'):
        t = r['departure_time'] or r['arrival_time']
        if not t or r['trip_id'] not in trip:
            continue
        h, m, s = map(int, t.split(':'))
        times[r['trip_id']].append((int(r['stop_sequence']), stop_name[r['stop_id']], h * 3600 + m * 60 + s))
    names = sorted({n for v in times.values() for _, n, _ in v})
    ni = {n: i for i, n in enumerate(names)}
    tables = {'routes': [], 'hs': [], 'svc': []}
    index = {k: {} for k in tables}
    def idx(kind, value):
        key = json.dumps(value)
        if key not in index[kind]:
            index[kind][key] = len(tables[kind])
            tables[kind].append(value)
        return index[kind][key]
    pats, pat_index, trips = [], {}, []
    m = [re.match(r'^(.*?)(\d+)$', t) for t in times]
    prefix = m[0].group(1) if m and all(x and x.group(1) == m[0].group(1) for x in m) else None
    for tid, v in times.items():
        v.sort()
        t0 = v[0][2]
        key = (tuple(ni[n] for _, n, _ in v), tuple((x - t0) // 60 for *_, x in v))
        if key not in pat_index:
            pat_index[key] = len(pats)
            pats.append([list(key[0]), list(key[1])])
        r = trip[tid]
        trips.append([idx('routes', list(route[r['route_id']])), idx('hs', r['trip_headsign'].strip()),
                      idx('svc', r['service_id']), pat_index[key], t0 // 60,
                      int(tid[len(prefix):]) if prefix is not None else tid])
    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    cal = [[r['service_id'], r['start_date'], r['end_date'], ''.join(r[d] for d in days)] for r in rows('calendar.txt')]
    ex = [[r['service_id'], r['date'], r['exception_type']] for r in rows('calendar_dates.txt')]
    feed = next(iter(rows('feed_info.txt')), {})
    end = feed.get('feed_end_date') or max((c[2] for c in cal), default='')
    return dict(end=end, tp=prefix or '', names=names, pats=pats, trips=trips, cal=cal, ex=ex, **tables)

if __name__ == '__main__':
    aut, nav, out = sys.argv[1:4]
    data = {'aut': convert(aut), 'nav': convert(nav)}
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(data, f, separators=(',', ':'), ensure_ascii=False)
    print('OK:', len(data['aut']['trips']), 'corse bus,', len(data['nav']['trips']), 'corse battelli')
