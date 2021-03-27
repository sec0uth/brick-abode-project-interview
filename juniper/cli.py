from jnpr.junos import Device
from jnpr.junos import utils
from jnpr.junos.op.routes import RouteTable


def get_machine_info(facts):
    print(f'Version: {facts.get("version")}')
    print(f'Model: {facts.get("model")}')
    print(f'Name: {facts.get("fqdn")}')


def get_up_time(facts):
    re0 = facts.get('RE0')

    if re0 is not None:
        print(f'Uptime: {re0.get("up_time")}')


def get_basic_routing_table(dev):
    route_info = dev.rpc.get_route_information()
    entries = (list(el.getiterator()) for el in route_info.getiterator()
                if el.tag == 'rt')

    mask = '{:<12} {:<10} {:<8}'
    headers = ['To', 'Via', 'Interface']
    columns = []

    for route_entries in entries:
        rt_type = route_entries[6].text
        if rt_type in ['INET6']:
            continue

        routes = [route_entries[1].text]

        if len(route_entries) > 12:
            via = route_entries[-2].text
        else:
            via = route_entries[10].text

        routes.append(via)
        routes.append(route_entries[-1].text)

        routes = ['None' if route is None else route
                  for route in routes]

        columns.append(routes)

    print(mask.format(*headers))
    for routes in columns:
        print(mask.format(*routes))


def get_routing_table_the_right_way(dev):
    rt_table = RouteTable(dev).get()

    mask = '{:<12} {:<10} {:<8}'
    headers = ['To', 'Via', 'Interface']
    columns = []
    
    for route, meta in rt_table.items():
        rt_meta = dict(meta)
        if rt_meta['protocol'] in ['INET6']:
            continue

        columns.append([route,
                        rt_meta['nexthop'] or 'None',
                        rt_meta['via']])

    print(mask.format(*headers))
    for routes in columns:
        print(mask.format(*routes))


def device():
    return Device(host='juniper', port=22)


with device() as jnpr_dev:
    facts = jnpr_dev.facts

    get_machine_info(facts)
    get_up_time(facts)
    get_basic_routing_table(jnpr_dev)
    
    get_routing_table_the_right_way(jnpr_dev)