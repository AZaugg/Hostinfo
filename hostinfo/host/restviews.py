from .models import Host, AllowedKey, KeyValue, HostAlias, Links
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods


###############################################################################
@require_http_methods(["GET"])
def HostDetail(request, pk=None, name=None):
    if pk:
        hostid = get_object_or_404(Host, id=pk)
    elif name:
        hostid = get_object_or_404(Host, hostname=name)
    return JsonResponse(HostSerialize(hostid, request))


###############################################################################
@require_http_methods(["GET"])
def HostList(request):
    hosts = get_list_or_404(Host)
    ans = [HostShortSerialize(h, request) for h in hosts]
    return JsonResponse(ans, safe=False)


###############################################################################
@require_http_methods(["GET"])
def KeyDetail(request, pk=None, name=None):
    if pk:
        keyid = get_object_or_404(AllowedKey, id=pk)
    elif name:
        keyid = get_object_or_404(AllowedKey, key=name)
    return JsonResponse(AllowedKeySerialize(keyid, request))


###############################################################################
@require_http_methods(["GET"])
def AliasDetail(request, pk=None, name=None):
    if pk:
        keyid = get_object_or_404(HostAlias, id=pk)
    elif name:
        keyid = get_object_or_404(HostAlias, alias=name)
    return JsonResponse(HostAliasSerialize(keyid, request))


###############################################################################
@require_http_methods(["GET"])
def KValDetail(request, pk=None):
    keyid = get_object_or_404(KeyValue, id=pk)
    return JsonResponse(KeyValueSerialize(keyid, request))


###############################################################################
def HostSerialize(obj, request):
    keys = {}
    for ak in AllowedKey.objects.all():
        keys[ak.id] = ak.key
    keyvals = {}
    for k in KeyValue.objects.filter(hostid=obj):
        keyname = keys[k.keyid_id]
        if keyname not in keyvals:
            keyvals[keyname] = []
        keyvals[keyname].append(KeyValueSerialize(k, request))

    aliases = []
    for h in HostAlias.objects.filter(hostid=obj):
        aliases.append(HostAliasSerialize(h, request))
    links = []
    for l in Links.objects.filter(hostid=obj):
        links.append(LinkSerialize(l, request))

    ans = {
        'id': obj.id,
        'name': obj.hostname,
        'origin': obj.origin,
        'createdate': obj.createdate,
        'modifieddate': obj.modifieddate,
        'keyvalues': keyvals,
        'aliases': aliases,
        'links': links,
        }
    return ans


###############################################################################
def AllowedKeySerialize(obj, request):
    ans = {
        'id': obj.id,
        'url': request.build_absolute_uri(reverse('restkey', args=(obj.id,))),
        'key': obj.key,
        'validtype': obj.get_validtype_display(),
        'desc': obj.desc,
        'createdate': obj.createdate,
        'modifieddate': obj.modifieddate,
        'restricted': obj.restrictedFlag,
        'audit': obj.auditFlag
    }
    return ans


###############################################################################
def HostShortSerialize(obj, request):
    return {
        'hostid': obj.id,
        'hostname': obj.hostname,
        'url': request.build_absolute_uri(reverse('resthost', args=(obj.id,))),
    }


###############################################################################
def LinkSerialize(obj, request):
    ans = {
        'id': obj.id,
        'host': HostShortSerialize(obj.hostid, request),
        'url': obj.url,
        'tag': obj.url,
        'modifieddate': obj.modifieddate
    }
    return ans


###############################################################################
def KeyValueSerialize(obj, request):
    ans = {
        'id': obj.id,
        'url': request.build_absolute_uri(reverse('restkval', args=(obj.id,))),
        'host': HostShortSerialize(obj.hostid, request),
        'keyid': obj.keyid.id,
        'key': obj.keyid.key,
        'value': obj.value,
        'origin': obj.origin,
        'createdate': obj.createdate,
        'modifieddate': obj.modifieddate
    }
    return ans


###############################################################################
def HostAliasSerialize(obj, request):
    ans = {
        'id': obj.id,
        'url': request.build_absolute_uri(reverse('restalias', args=(obj.id,))),
        'host': HostShortSerialize(obj.hostid, request),
        'alias': obj.alias,
        'origin': obj.origin,
        'createdate': obj.createdate,
        'modifieddate': obj.modifieddate
        }
    return ans

# EOF
