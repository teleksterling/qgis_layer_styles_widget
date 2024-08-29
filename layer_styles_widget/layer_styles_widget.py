# -*- coding: utf-8 -*-
"""QGIS Layer Styles Widget

.. note:: This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""

__author__ = '(C) 2024 by Rick Williams'
__date__ = '29/08/2024'
__copyright__ = 'Copyright 2024, Rick Williams'
# This will get replaced with a git SHA1 when you do a git archive
__revision__ = '$Format:%H$'

import os
from qgis.PyQt.QtCore import (
    QTranslator,
    QCoreApplication
)
from qgis.PyQt.QtWidgets import (
    # QWidget,
    # QCheckBox,
    # QHBoxLayout,
    # QSpacerItem,
    # QSizePolicy,
    QComboBox
)
from qgis.core import (
    # QgsMapLayer,
    QgsApplication
)
from qgis.gui import (
    QgisInterface,
    QgsGui,
    QgsLayerTreeEmbeddedWidgetProvider
)

VERSION = '1.0.0'


class LayerStylesComboBox(QComboBox):
    """
    Layer tree widget for changing layer style
    """
    def __init__(self, layer):
        QComboBox.__init__(self)
        self.layer = layer
        for style_name in layer.styleManager().styles():
            self.addItem(style_name)

        # self.setAutoFillBackground(False)
        # self.checkbox = QCheckBox(self.tr("Show Labels"))
        # layout = QHBoxLayout()
        # spacer = QSpacerItem(1, 0, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        # layout.addWidget(self.checkbox)
        # layout.addItem(spacer)
        # self.setLayout(layout)

        # init from layer
        idx = self.findText(layer.styleManager().currentStyle())
        if idx != -1:
          self.setCurrentIndex(idx)

        self.currentIndexChanged.connect(self.on_current_changed)

    def on_current_changed(self, index):
        self.layer.styleManager().setCurrentStyle(self.itemText(index))
        # self.layer.triggerRepaint()

class LayerStylesWidgetProvider(QgsLayerTreeEmbeddedWidgetProvider):
    def __init__(self):
        QgsLayerTreeEmbeddedWidgetProvider.__init__(self)

    def id(self):
        return "style"

    def name(self):
        return "Layer style selector"

    def createWidget(self, layer, widgetIndex):
        return LayerStylesComboBox(layer)

    def supportsLayer(self, layer):
        return True   # any layer is fine


class LayerStylesWidgetPlugin:
    """QGIS Plugin Implementation."""

    def __init__(self, iface: QgisInterface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        super().__init__()
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QgsApplication.locale()
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            '{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        self.provider = None

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        self.provider = LayerStylesWidgetProvider()
        QgsGui.layerTreeEmbeddedWidgetRegistry().addProvider(self.provider)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        QgsGui.layerTreeEmbeddedWidgetRegistry().removeProvider(self.provider.id())
        self.provider = None
