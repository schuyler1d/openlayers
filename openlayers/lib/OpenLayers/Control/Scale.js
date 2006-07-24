/* Copyright (c) 2006 MetaCarta, Inc., published under the BSD license.
 * See http://svn.openlayers.org/trunk/openlayers/license.txt for the full
 * text of the license. */

// @require: OpenLayers/Control.js

/**
 * @class
 */
OpenLayers.Control.Scale = Class.create();
OpenLayers.Control.Scale.prototype = 
  Object.extend( new OpenLayers.Control(), {
    INCHES_PER_UNIT: { // borrowed from MapServer mapscale.c
	inches: 1.0,
	ft: 12.0,
	mi: 63360.0,
	m: 39.3701,
	km: 39370.1,
	dd: 4374754
    },

    /** @type DOMElement */
    element: null,
    
    /** @type String */
    units: 'dd',
    
    /** @type Integer */
    dpi: 72,

    /**
     * @constructor
     * 
     * @param {DOMElement} element
     * @param {String} base
     */
    initialize: function(element, units) {
        OpenLayers.Control.prototype.initialize.apply(this, arguments);
        this.element = element;        
        if (units) this.units = units;
    },

    /**
     * @type DOMElement
     */    
    draw: function() {
        OpenLayers.Control.prototype.draw.apply(this, arguments);
        if (!this.element) {
            this.element = document.createElement("div");
            this.div.style.right = "3px";
            this.div.style.bottom = "2em";
            this.div.style.left = "";
            this.div.style.top = "";
            this.div.style.display = "block";
            this.div.style.position = "absolute";
            this.element.style.fontSize="smaller";
            this.div.appendChild(this.element);
        }
        this.map.events.register( 'moveend', this, this.updateScale);
	this.updateScale();
        return this.div;
    },
   
    /**
     * 
     */
    updateScale: function() {
        var res = this.map.getResolution();
	if (!res) return;

	var scale = res * this.INCHES_PER_UNIT[this.units] * this.dpi;
	if (scale >= 9500 && scale <= 950000) {
	    scale = Math.round(scale / 1000) + "K";
	} else if (scale >= 950000) {
	    scale = Math.round(scale / 1000000) + "M";
	} else {
	    scale = Math.round(scale / 100) * 100;
	}
        this.element.innerHTML = "Scale = 1 : " + scale;
    }, 
    
    /** @final @type String */
    CLASS_NAME: "OpenLayers.Control.Scale"
});
