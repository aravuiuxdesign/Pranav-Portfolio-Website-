/* dc-lite: a small standalone runtime for the portfolio's Design Component pages.
   Supports {{holes}} in text and attributes, on*="{{fn}}" events, ref="{{fn}}",
   <sc-if value>, <sc-for list as>, and class Component extends DCLogic with
   state / setState / renderVals / componentDidMount. Updates the DOM in place. */
(function () {
  'use strict';
  var HOLE = /\{\{\s*([^}]+?)\s*\}\}/g;
  var ONE = /^\s*\{\{\s*([^}]+?)\s*\}\}\s*$/;

  function lookup(path, scope) {
    path = path.trim();
    if (path === 'true') return true;
    if (path === 'false') return false;
    if (path === 'null') return null;
    if (/^-?\d+(\.\d+)?$/.test(path)) return +path;
    var parts = path.split('.'), v, found = false;
    for (var i = scope.length - 1; i >= 0; i--) {
      var s = scope[i];
      if (s && parts[0] in s) { v = s[parts[0]]; found = true; break; }
    }
    if (!found) return undefined;
    for (var k = 1; k < parts.length; k++) { if (v == null) return undefined; v = v[parts[k]]; }
    return v;
  }
  function interp(str, scope) {
    var m = str.match(ONE);
    if (m) return lookup(m[1], scope);
    return str.replace(HOLE, function (_, p) { var v = lookup(p, scope); return v == null ? '' : String(v); });
  }
  function hasHole(s) { HOLE.lastIndex = 0; return s.indexOf('{{') !== -1 && /\{\{[^}]+\}\}/.test(s); }

  // Build nodes for the children of a template node. Returns {nodes, update(scope)}
  function buildChildren(tplParent, ctx) {
    var nodes = [], binds = [];
    for (var c = tplParent.firstChild; c; c = c.nextSibling) buildNode(c, nodes, binds, ctx);
    return { nodes: nodes, update: function (scope) { for (var i = 0; i < binds.length; i++) binds[i](scope); } };
  }
  function insertAfter(anchor, nodes) {
    var ref = anchor.nextSibling, p = anchor.parentNode;
    for (var i = 0; i < nodes.length; i++) p.insertBefore(nodes[i], ref);
  }
  function removeNodes(nodes) { for (var i = 0; i < nodes.length; i++) if (nodes[i].parentNode) nodes[i].parentNode.removeChild(nodes[i]); }

  function buildNode(t, out, binds, ctx) {
    if (t.nodeType === 3) {
      var txt = document.createTextNode(t.data);
      out.push(txt);
      if (hasHole(t.data)) {
        var src = t.data;
        binds.push(function (scope) { var v = interp(src, scope); var s = v == null || v === false ? '' : String(v); if (txt.data !== s) txt.data = s; });
      }
      return;
    }
    if (t.nodeType === 8) { out.push(document.createComment(t.data)); return; }
    if (t.nodeType !== 1) return;
    var tag = t.localName;

    if (tag === 'sc-if') {
      var a = document.createComment('if'); out.push(a);
      var cond = t.getAttribute('value') || '', blk = null;
      binds.push(function (scope) {
        var v = interp(cond, scope);
        if (v && !blk) { blk = buildChildren(t, ctx); blk.update(scope); insertAfter(a, blk.nodes); }
        else if (!v && blk) { removeNodes(blk.nodes); blk = null; }
        else if (blk) blk.update(scope);
      });
      return;
    }
    if (tag === 'sc-for') {
      var end = document.createComment('for'); out.push(end);
      var listExpr = t.getAttribute('list') || '', as = t.getAttribute('as') || 'item', items = [];
      binds.push(function (scope) {
        var list = interp(listExpr, scope) || [];
        for (var i = 0; i < list.length; i++) {
          var o = {}; o[as] = list[i]; o[as + 'Index'] = i; o.index = i;
          var sc = scope.concat([o]);
          if (!items[i]) {
            items[i] = buildChildren(t, ctx);
            items[i].update(sc);
            var p = end.parentNode;
            for (var j = 0; j < items[i].nodes.length; j++) p.insertBefore(items[i].nodes[j], end);
          } else items[i].update(sc);
        }
        while (items.length > list.length) removeNodes(items.pop().nodes);
      });
      return;
    }

    var el = t.cloneNode(false);
    var attrs = Array.prototype.slice.call(t.attributes);
    attrs.forEach(function (at) {
      var name = at.name, val = at.value;
      if (name.indexOf('hint-') === 0) { el.removeAttribute(name); return; }
      if (!hasHole(val)) return;
      el.removeAttribute(name);
      var m = val.match(ONE);
      if (name === 'ref' && m) {
        var done = false, path = m[1];
        binds.push(function (scope) { if (done) return; var f = lookup(path, scope); if (typeof f === 'function') { done = true; ctx.refs.push(function () { f(el); }); } });
        return;
      }
      if (name.length > 2 && name.indexOf('on') === 0 && m) {
        var evt = name.slice(2).toLowerCase(), epath = m[1], cur = null;
        el.addEventListener(evt, function (e) { var f = cur && lookup(epath, cur); if (typeof f === 'function') return f(e); });
        binds.push(function (scope) { cur = scope; });
        return;
      }
      binds.push(function (scope) {
        var v = interp(val, scope);
        if (v === false || v == null) { if (el.hasAttribute(name)) el.removeAttribute(name); }
        else { var s = v === true ? '' : String(v); if (el.getAttribute(name) !== s) el.setAttribute(name, s); }
        if (name === 'value' && 'value' in el) el.value = v == null ? '' : v;
        if (name === 'checked' && 'checked' in el) el.checked = !!v;
      });
    });
    var kids = buildChildren(t, ctx);
    for (var i = 0; i < kids.nodes.length; i++) el.appendChild(kids.nodes[i]);
    binds.push(kids.update);
    out.push(el);
  }

  function DCLogic(props) { this.props = props || {}; this.state = {}; }
  DCLogic.prototype.setState = function (p, cb) {
    var self = this;
    var patch = typeof p === 'function' ? p(this.state, this.props) : p;
    this.state = Object.assign({}, this.state, patch);
    if (this.__sched) { if (cb) this.__cbs.push(cb); return; }
    this.__sched = true; this.__cbs = cb ? [cb] : [];
    Promise.resolve().then(function () {
      self.__sched = false;
      if (self.__update) self.__update();
      var cbs = self.__cbs; self.__cbs = [];
      cbs.forEach(function (f) { try { f(); } catch (e) { console.error(e); } });
      if (typeof self.componentDidUpdate === 'function') { try { self.componentDidUpdate(); } catch (e) { console.error(e); } }
    });
  };
  DCLogic.prototype.forceUpdate = function () { if (this.__update) this.__update(); };
  DCLogic.prototype.renderVals = function () { return {}; };
  window.DCLogic = DCLogic;

  function boot() {
    var tpl = document.getElementById('dc-tpl');
    var scriptEl = document.querySelector('script[data-dc-script]');
    if (!tpl || !scriptEl) return;
    var content = tpl.content;
    // helmet -> head
    var helmet = content.querySelector('helmet');
    if (helmet) {
      Array.prototype.slice.call(helmet.childNodes).forEach(function (n) {
        if (n.nodeType !== 1) return;
        var copy;
        if (n.localName === 'script') { copy = document.createElement('script'); Array.prototype.forEach.call(n.attributes, function (a) { copy.setAttribute(a.name, a.value); }); copy.textContent = n.textContent; }
        else copy = document.importNode(n, true);
        document.head.appendChild(copy);
      });
      helmet.parentNode.removeChild(helmet);
    }
    var props = {};
    try {
      var decl = JSON.parse(scriptEl.getAttribute('data-props') || '{}');
      Object.keys(decl).forEach(function (k) { if (k[0] !== '$' && decl[k] && 'default' in decl[k]) props[k] = decl[k].default; });
    } catch (e) { console.error('data-props', e); }
    var over = window.__DC_PROPS__ || {};
    Object.keys(over).forEach(function (k) { props[k] = over[k]; });

    var Component;
    try { Component = new Function('DCLogic', scriptEl.textContent + '\n;return Component;')(DCLogic); }
    catch (e) { console.error('component script', e); return; }
    var c = new Component(props);
    if (!c.state) c.state = {};
    var ctx = { refs: [] };
    var root = buildChildren(content, ctx);
    var frag = document.createDocumentFragment();
    root.nodes.forEach(function (n) { frag.appendChild(n); });
    var vals = c.renderVals() || {};
    root.update([vals]);
    document.body.insertBefore(frag, tpl);
    var runRefs = function () { var r = ctx.refs; ctx.refs = []; r.forEach(function (f) { try { f(); } catch (e) { console.error(e); } }); };
    runRefs();
    c.__update = function () { root.update([c.renderVals() || {}]); runRefs(); };
    document.documentElement.classList.add('dc-ready');
    if (typeof c.componentDidMount === 'function') { try { c.componentDidMount(); } catch (e) { console.error('componentDidMount', e); } }
    window.__dc = c;
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
