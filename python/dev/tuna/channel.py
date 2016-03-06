
import pygtk
pygtk.require('2.0')
import gtk
import numpy as np

class index:
    SP    =  0 # input charge polarity
    SC    =  1 # large sensor capacitance mode
    SL    =  2 # leakage current disable
    ST    =  3 # test capacitor enable 
    SM    =  4 # mask enable
    SD    =  5 # threshold DAC
    SMX   =  9 # channel monitor mode
    SZ10b = 10 # 10-bit ADC
    SZ8b  = 15 #  8-bit ADC
    SZ6b  = 19 #  6-bit ADC

class Channel:

    def __init__(self, channel_number):

        self.chan_val    = np.zeros((24), dtype=int)
        self.channel_box = gtk.HBox(homogeneous=False, spacing=0)
        self.glabel      = gtk.Label("%02i" % channel_number)
        self.button_SP   = gtk.ToggleButton(label="n")
        self.button_SC   = gtk.CheckButton()
        self.button_SL   = gtk.CheckButton()
        self.button_ST   = gtk.CheckButton()
        self.button_SM   = gtk.CheckButton()
        self.button_SMX  = gtk.CheckButton()
        self.combo_SD    = gtk.combo_box_new_text()
        self.combo_SZ10b = gtk.combo_box_new_text()
        self.combo_SZ8b  = gtk.combo_box_new_text()
        self.combo_SZ6b  = gtk.combo_box_new_text()

        for i in range(16):
            self.combo_SD.append_text(str(i) + " mv")
        for i in range(32):
            self.combo_SZ10b.append_text(str(i) + " ns")        
        for i in range(16):
            self.combo_SZ8b.append_text(str(i) + " ns")        
        for i in range(8):
            self.combo_SZ6b.append_text(str(i) + " ns")        
        for combo in [self.combo_SD, self.combo_SZ10b, self.combo_SZ8b, self.combo_SZ6b]:
            combo.set_active(0)

        self.button_SP.connect(  "toggled", self.SP_callback)
        self.button_SC.connect(  "toggled", self.generic_callback, index.SC)
        self.button_SL.connect(  "toggled", self.generic_callback, index.SL)
        self.button_ST.connect(  "toggled", self.generic_callback, index.ST)
        self.button_SM.connect(  "toggled", self.generic_callback, index.SM)
        self.button_SMX.connect( "toggled", self.generic_callback, index.SMX)
        self.combo_SD.connect(   "changed", self.get_SD_value)
        self.combo_SZ10b.connect("changed", self.get_SZ10b_value)
        self.combo_SZ8b.connect( "changed", self.get_SZ8b_value)
        self.combo_SZ6b.connect( "changed", self.get_SZ6b_value)

        self.button_SM.set_active(True)
        
        for obj in [self.glabel, 
                    self.button_SP,
                    self.button_SC,
                    self.button_SL,
                    self.button_ST,
                    self.button_SM,
                    self.combo_SD,
                    self.button_SMX,
                    self.combo_SZ10b,
                    self.combo_SZ8b,
                    self.combo_SZ6b,
                    ]:
            self.channel_box.pack_start(obj, expand=False)
            
    def get_chan_val(self):
        return self.chan_val

    def generic_callback(self, widget, ind):
        self.chan_val[ind] = 1 if widget.get_active() else 0

    def SP_callback(self, widget):
        self.chan_val[index.SP] = 1 if widget.get_active() else 0
        widget.set_label("p"        if widget.get_active() else "n")

    def get_SD_value(self, widget):
        word = '{0:04b}'.format(widget.get_active())
        for bit in xrange(len(word)):
            self.globalreg[index.SD + bit] = int(word[bit])

    def get_SZ10b_value(self, widget):
        word = '{0:05b}'.format(widget.get_active())
        for bit in xrange(len(word)):
            self.globalreg[index.SZ10b + bit] = int(word[bit])

    def get_SZ8b_value(self, widget):
        word = '{0:04b}'.format(widget.get_active())
        for bit in xrange(len(word)):
            self.globalreg[index.SZ8b + bit] = int(word[bit])

    def get_SZ6b_value(self, widget):
        word = '{0:03b}'.format(widget.get_active())
        for bit in xrange(len(word)):
            self.globalreg[index.SZ6b + bit] = int(word[bit])

