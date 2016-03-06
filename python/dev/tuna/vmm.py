
import pygtk
pygtk.require('2.0')
import gtk
import numpy as np

from channel import Channel

class registers:
    SPG    = 16 # input charge polarity
    SDP    = 17 # disable at peak
    SBMX   = 18 # route analog monitor to pdo output
    SBFT   = 19 # analog output buffers enable tdo
    SBFP   = 20 # analog output buffers enable pdo
    SBFM   = 21 # analog output buffers enable mo
    SLG    = 22 # leakage current disable
    SM     = 23 # monitor multiplexing
    SCMX   = 29 # monitor multiplexing enable
    SFA    = 30 # ART enable
    SFAM   = 31 # ART mode
    ST     = 32 # peaking time
    SFM    = 34 # UNKNOWN
    SG     = 35 # gain
    SNG    = 38 # neighbor triggering enable
    STOT   = 39 # timing outputs control
    STTT   = 40 # timing outputs enable
    SSH    = 41 # sub-hysteresis discrimination enable
    STC    = 42 # TAC slope adjustment
    SDT    = 44 # course threshold DAC
    SDP    = 54 # test pulse DAC
    SC10b  = 65 # 10-bit ADC conversion time
    SC8b   = 67 # 8-bit ADC conversion time
    SC6b   = 70 # 6-bit ADC conversion time
    S8b    = 71 # 8-bit ADC conversion mode
    S6b    = 72 # 6-bit ADC conversion enable
    SPDC   = 73 # ADCs enable
    SDCKS  = 74 # dual clock edge serialized data enable
    SDCKA  = 75 # dual clock edge serialized ART enable
    SDCK6b = 76 # dual clock edge serialized 6-bit enable
    SDRV   = 77 # tristates analog outputs with token, used in analog mode
    STPP   = 78 # timing outputs control 2

class VMM:

    def get_channel_val(self):
        for ch_num in range(64):
            chan_val = self.chan_list[ch_num].get_chan_val()
            for i in range(24):
                self.reg[ch_num][i] = chan_val[i]
        return self.reg

    # quick set functions
    def SP_qs_callback(self, widget):
        widget.set_label("p" if widget.get_active() else "n")

    def quick_set(self, widget):

        for chan in self.chan_list:

            if self.check_button_SP_qs.get_active():
                chan.button_SP.set_active(True if self.toggle_button_SP.get_active() else False)
                chan.button_SP.set_label("p"   if self.toggle_button_SP.get_active() else "n")

            if self.check_button_SC_qs.get_active():    chan.button_SC.set_active(self.check_button_SC.get_active())
            if self.check_button_SL_qs.get_active():    chan.button_SL.set_active(self.check_button_SL.get_active())
            if self.check_button_ST_qs.get_active():    chan.button_ST.set_active(self.check_button_ST.get_active())
            if self.check_button_SM_qs.get_active():    chan.button_SM.set_active(self.check_button_SM.get_active())
            if self.check_button_SD_qs.get_active():    chan.combo_SD.set_active(self.combo_SD_qs.get_active())
            if self.check_button_SMX_qs.get_active():   chan.button_SMX.set_active(self.check_button_SMX.get_active())
            if self.check_button_SZ10b_qs.get_active(): chan.combo_SZ10b.set_active(self.combo_SZ10b_qs.get_active())
            if self.check_button_SZ8b_qs.get_active():  chan.combo_SZ8b.set_active(self.combo_SZ8b_qs.get_active())
            if self.check_button_SZ6b_qs.get_active():  chan.combo_SZ6b.set_active(self.combo_SZ6b_qs.get_active())
    
    def glob_callback(self, widget, register):
        self.globalreg[register] = 1 if widget.get_active() else 0

    def glob_SM_value(self, widget):
        word = '{0:06b}'.format(widget.get_active())
        for bit in xrange(len(word)):
            self.globalreg[registers.SM + bit] = int(word[bit])

    def glob_ST_value(self, widget):
        word = '{0:02b}'.format(widget.get_active())
        for bit in xrange(len(word)):
            self.globalreg[registers.ST + bit] = int(word[bit])

    def glob_SG_value(self, widget):
        word = '{0:03b}'.format(widget.get_active())
        for bit in xrange(len(word)):
            self.globalreg[registers.SG + bit] = int(word[bit])

    def glob_STC_value(self, widget):
        word = '{0:02b}'.format(widget.get_active())
        for bit in xrange(len(word)):
            self.globalreg[registers.STC + bit] = int(word[bit])

    def glob_SDT_entry(self, widget, entry):
        value = int(widget.get_text())
        if value < 0 or value > 1023:
            sys.exit("SDT value out of range")
        word = '{0:010b}'.format(value)
        for bit in xrange(len(word)):
            self.globalreg[registers.SDT + bit] = int(word[bit])

    def glob_SDP_entry(self, widget, entry):
        value = int(widget.get_text())
        if value < 0 or value > 1023:
            sys.exit("SDP value out of range")
        word = '{0:010b}'.format(value)
        for bit in xrange(len(word)):
            self.globalreg[registers.SDP + bit] = int(word[bit])

    def glob_SC10b_value(self, widget):
        word = '{0:02b}'.format(widget.get_active())
        for bit in xrange(len(word)):
            self.globalreg[registers.SC10b - bit] = int(word[bit]) # reversed!

    def glob_SC8b_value(self, widget):
        word = '{0:02b}'.format(widget.get_active())
        for bit in xrange(len(word)):
            self.globalreg[registers.SC8b - bit] = int(word[bit]) # reversed!

    def glob_SC6b_value(self, widget):
        word = '{0:03b}'.format(widget.get_active())
        for bit in xrange(len(word)):
            self.globalreg[registers.SC6b - bit] = int(word[bit]) # reversed!

    def __init__(self):
        self.channel_settings = np.zeros((64, 24), dtype=int)
        self.global_settings  = np.zeros((96),     dtype=int)
        self.chan_list = []
        self.reg = np.zeros((64, 24), dtype=int)
        self.msg = np.zeros((67), dtype=np.uint32)
        self.globalreg = np.zeros((96), dtype=int)
        
        #%%%%%%%%%%%%%%%%%%  VMM WIDGETS  %%%%%%%%%%%%%%%%%%%%%
        #                    64 CHANNELS 
        #                  CHANNEL LABELS 
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        self.label_channels = gtk.Label("Channel Configuration")
        self.label_channels.set_markup('<span color="green" size="18000"><b>Channel Configuration</b></span>')
        self.box_channels = gtk.HBox()
        self.box_channels.pack_start(self.label_channels, expand=False)

        self.label_Chan_num_a = gtk.Label("    \n   ")
        self.label_Chan_SP_a = gtk.Label("     S \n     P ")
        self.label_Chan_SP_a.set_markup('<span color="green"><b>  S \n  P </b></span>')
        self.label_Chan_SC_a = gtk.Label("S\nC")
        self.label_Chan_SC_a.set_markup('<span color="green"><b> S \n C </b></span>')
        self.label_Chan_ST_a = gtk.Label("S\nL")
        self.label_Chan_ST_a.set_markup('<span color="green"><b> S \n L</b></span>')
        self.label_Chan_SL_a = gtk.Label("S\nT")
        self.label_Chan_SL_a.set_markup('<span color="green"><b>  S \n  T </b></span>')
        self.label_Chan_SM_a = gtk.Label("S\nM")
        self.label_Chan_SM_a.set_markup('<span color="green"><b> S    \n M     </b></span>')
        self.label_Chan_SD_a = gtk.Label("SD")
        self.label_Chan_SD_a.set_markup('<span color="green"><b>  SD     </b></span>')
        self.label_Chan_SMX_a = gtk.Label("S\nM\nX")
        self.label_Chan_SMX_a.set_markup('<span color="green"><b> S  \n M  \n X  </b></span>')
        self.label_Chan_SZ10b_a = gtk.Label("SZ10b")
        self.label_Chan_SZ10b_a.set_markup('<span color="green"><b>  SZ10b   </b></span>')
        self.label_Chan_SZ8b_a = gtk.Label("SZ8b")
        self.label_Chan_SZ8b_a.set_markup('<span color="green"><b>  SZ8b    </b></span>')
        self.label_Chan_SZ6b_a = gtk.Label("SZ6b")        
        self.label_Chan_SZ6b_a.set_markup('<span color="green"><b>  SZ6b    </b></span>')

        self.box_chan_labels_a = gtk.HBox()
        self.box_chan_labels_a.pack_start(self.label_Chan_num_a)
        self.box_chan_labels_a.pack_start(self.label_Chan_SP_a)
        self.box_chan_labels_a.pack_start(self.label_Chan_SC_a)
        self.box_chan_labels_a.pack_start(self.label_Chan_ST_a)
        self.box_chan_labels_a.pack_start(self.label_Chan_SL_a)
        self.box_chan_labels_a.pack_start(self.label_Chan_SM_a)
        self.box_chan_labels_a.pack_start(self.label_Chan_SD_a)
        self.box_chan_labels_a.pack_start(self.label_Chan_SMX_a)
        self.box_chan_labels_a.pack_start(self.label_Chan_SZ10b_a)
        self.box_chan_labels_a.pack_start(self.label_Chan_SZ8b_a)
        self.box_chan_labels_a.pack_start(self.label_Chan_SZ6b_a)

        self.label_Chan_num_b = gtk.Label("    \n   ")
        self.label_Chan_SP_b = gtk.Label("     S \n     P ")
        self.label_Chan_SP_b.set_markup('<span color="green"><b>  S \n  P </b></span>')
        self.label_Chan_SC_b = gtk.Label(" S \n C ")
        self.label_Chan_SC_b.set_markup('<span color="green"><b> S \n C </b></span>')
        self.label_Chan_ST_b = gtk.Label(" S \n L ")
        self.label_Chan_ST_b.set_markup('<span color="green"><b> S \n L </b></span>')
        self.label_Chan_SL_b = gtk.Label(" S \n T ")
        self.label_Chan_SL_b.set_markup('<span color="green"><b>  S \n  T </b></span>')
        self.label_Chan_SM_b = gtk.Label("S    \nM    ")
        self.label_Chan_SM_b.set_markup('<span color="green"><b> S    \n M     </b></span>')
        self.label_Chan_SD_b = gtk.Label("  SD     ")
        self.label_Chan_SD_b.set_markup('<span color="green"><b>  SD     </b></span>')
        self.label_Chan_SMX_b = gtk.Label(" S  \n M  \n X  ")
        self.label_Chan_SMX_b.set_markup('<span color="green"><b> S  \n M  \n X  </b></span>')
        self.label_Chan_SZ10b_b = gtk.Label("  SZ10b   ")
        self.label_Chan_SZ10b_b.set_markup('<span color="green"><b>  SZ10b   </b></span>')
        self.label_Chan_SZ8b_b = gtk.Label("  SZ8b    ")
        self.label_Chan_SZ8b_b.set_markup('<span color="green"><b>  SZ8b    </b></span>')
        self.label_Chan_SZ6b_b = gtk.Label("  SZ6b    ")        
        self.label_Chan_SZ6b_b.set_markup('<span color="green"><b>  SZ6b    </b></span>')

        self.box_chan_labels_b = gtk.HBox()
        self.box_chan_labels_b.pack_start(self.label_Chan_num_b)
        self.box_chan_labels_b.pack_start(self.label_Chan_SP_b)
        self.box_chan_labels_b.pack_start(self.label_Chan_SC_b)
        self.box_chan_labels_b.pack_start(self.label_Chan_ST_b)
        self.box_chan_labels_b.pack_start(self.label_Chan_SL_b)
        self.box_chan_labels_b.pack_start(self.label_Chan_SM_b)
        self.box_chan_labels_b.pack_start(self.label_Chan_SD_b)
        self.box_chan_labels_b.pack_start(self.label_Chan_SMX_b)
        self.box_chan_labels_b.pack_start(self.label_Chan_SZ10b_b)
        self.box_chan_labels_b.pack_start(self.label_Chan_SZ8b_b)
        self.box_chan_labels_b.pack_start(self.label_Chan_SZ6b_b)

        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #                     CHANNEL WIDGETS 
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
        for chan_num in range(64):
            self.chan_list.append(Channel(chan_num))

        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #                   QUICK SET WIDGETS   
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


        self.button_quick_set = gtk.Button("QUICK SET")
        self.button_quick_set.connect("clicked",self.quick_set)
        self.button_quick_set.set_sensitive(True)

        self.check_button_SP_qs = gtk.CheckButton()
        self.check_button_SC_qs = gtk.CheckButton()
        self.check_button_SL_qs = gtk.CheckButton()
        self.check_button_ST_qs = gtk.CheckButton()
        self.check_button_SM_qs = gtk.CheckButton()
        self.check_button_SD_qs = gtk.CheckButton()
        self.check_button_SMX_qs = gtk.CheckButton()
        self.check_button_SZ10b_qs = gtk.CheckButton()
        self.check_button_SZ8b_qs = gtk.CheckButton()
        self.check_button_SZ6b_qs = gtk.CheckButton()

        self.toggle_button_SP = gtk.ToggleButton(label="n")
        self.toggle_button_SP.connect("toggled",self.SP_qs_callback)
        self.check_button_SC = gtk.CheckButton()
        self.check_button_SL = gtk.CheckButton()
        self.check_button_ST = gtk.CheckButton()
        self.check_button_SM = gtk.CheckButton()
        self.combo_SD_qs = gtk.combo_box_new_text()
        self.check_button_SMX = gtk.CheckButton()
        self.combo_SZ10b_qs = gtk.combo_box_new_text()
        self.combo_SZ8b_qs = gtk.combo_box_new_text()
        self.combo_SZ6b_qs = gtk.combo_box_new_text()

        #self.label_Chan_num_qs = gtk.Label(" \n ")
        self.label_Chan_SP_qs = gtk.Label("SP")
        self.label_Chan_SC_qs = gtk.Label("SC")
        self.label_Chan_SL_qs = gtk.Label("SL")
        self.label_Chan_ST_qs = gtk.Label("ST")
        self.label_Chan_SM_qs = gtk.Label("SM")
        self.label_Chan_SD_qs = gtk.Label("SD")
        self.label_Chan_SMX_qs = gtk.Label("SMX")
        self.label_Chan_SZ10b_qs = gtk.Label("SZ10b")
        self.label_Chan_SZ8b_qs = gtk.Label("SZ8b")
        self.label_Chan_SZ6b_qs = gtk.Label("SZ6b")

        for i in range(16):
            self.combo_SD_qs.append_text(str(i) + " mv")
        self.combo_SD_qs.set_active(0)
        for i in range(32):
            self.combo_SZ10b_qs.append_text(str(i) + " ns")
        self.combo_SZ10b_qs.set_active(0)
        for i in range(16):
            self.combo_SZ8b_qs.append_text(str(i) + " ns")
        self.combo_SZ8b_qs.set_active(0)
        for i in range(8):
            self.combo_SZ6b_qs.append_text(str(i) + " ns")
        self.combo_SZ6b_qs.set_active(0)

        self.check_button_SP_qs.set_sensitive(True)
        self.check_button_SC_qs.set_sensitive(True)
        self.check_button_SL_qs.set_sensitive(True)
        self.check_button_ST_qs.set_sensitive(True)
        self.check_button_SM_qs.set_sensitive(True)
        self.check_button_SD_qs.set_sensitive(True)
        self.check_button_SMX_qs.set_sensitive(True)
        self.check_button_SZ10b_qs.set_sensitive(True)
        self.check_button_SZ8b_qs.set_sensitive(True)
        self.check_button_SZ6b_qs.set_sensitive(True)

        self.toggle_button_SP.set_sensitive(True)
        self.check_button_SC.set_sensitive(True)
        self.check_button_SL.set_sensitive(True)
        self.check_button_ST.set_sensitive(True)
        self.check_button_SM.set_sensitive(True)
        self.combo_SD_qs.set_sensitive(True)
        self.check_button_SMX.set_sensitive(True)
        self.combo_SZ10b_qs.set_sensitive(True)
        self.combo_SZ8b_qs.set_sensitive(True)
        self.combo_SZ6b_qs.set_sensitive(True)

        self.qs_table = gtk.Table(rows=5, columns=10, homogeneous=False)
        self.qs_table.attach(self.label_Chan_SP_qs, left_attach=0, right_attach=1, top_attach=0, bottom_attach=1, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SP_qs, left_attach=0, right_attach=1, top_attach=1, bottom_attach=2, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.toggle_button_SP, left_attach=0, right_attach=1, top_attach=2, bottom_attach=3, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.label_Chan_SC_qs, left_attach=1, right_attach=2, top_attach=0, bottom_attach=1, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SC_qs, left_attach=1, right_attach=2, top_attach=1, bottom_attach=2, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SC, left_attach=1, right_attach=2, top_attach=2, bottom_attach=3, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.label_Chan_SL_qs, left_attach=2, right_attach=3, top_attach=0, bottom_attach=1, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SL_qs, left_attach=2, right_attach=3, top_attach=1, bottom_attach=2, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SL, left_attach=2, right_attach=3, top_attach=2, bottom_attach=3, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.label_Chan_ST_qs, left_attach=3, right_attach=4, top_attach=0, bottom_attach=1, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_ST_qs, left_attach=3, right_attach=4, top_attach=1, bottom_attach=2, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_ST, left_attach=3, right_attach=4, top_attach=2, bottom_attach=3, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.label_Chan_SM_qs, left_attach=4, right_attach=5, top_attach=0, bottom_attach=1, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SM_qs, left_attach=4, right_attach=5, top_attach=1, bottom_attach=2, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SM, left_attach=4, right_attach=5, top_attach=2, bottom_attach=3, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.label_Chan_SD_qs, left_attach=5, right_attach=6, top_attach=0, bottom_attach=1, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SD_qs, left_attach=5, right_attach=6, top_attach=1, bottom_attach=2, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.combo_SD_qs, left_attach=5, right_attach=6, top_attach=2, bottom_attach=3, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.label_Chan_SMX_qs, left_attach=6, right_attach=7, top_attach=0, bottom_attach=1, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SMX_qs, left_attach=6, right_attach=7, top_attach=1, bottom_attach=2, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SMX, left_attach=6, right_attach=7, top_attach=2, bottom_attach=3, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.label_Chan_SZ10b_qs, left_attach=7, right_attach=8, top_attach=0, bottom_attach=1, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SZ10b_qs, left_attach=7, right_attach=8, top_attach=1, bottom_attach=2, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.combo_SZ10b_qs, left_attach=7, right_attach=8, top_attach=2, bottom_attach=3, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.label_Chan_SZ8b_qs, left_attach=8, right_attach=9, top_attach=0, bottom_attach=1, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SZ8b_qs, left_attach=8, right_attach=9, top_attach=1, bottom_attach=2, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.combo_SZ8b_qs, left_attach=8, right_attach=9, top_attach=2, bottom_attach=3, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.label_Chan_SZ6b_qs, left_attach=9, right_attach=10, top_attach=0, bottom_attach=1, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SZ6b_qs, left_attach=9, right_attach=10, top_attach=1, bottom_attach=2, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.combo_SZ6b_qs, left_attach=9, right_attach=10, top_attach=2, bottom_attach=3, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.button_quick_set, left_attach=0, right_attach=10, top_attach=4, bottom_attach=5, xpadding=0,  ypadding=0)

        ##################### vmm Global ###################
        ##################### variables  ###################

        self.label_Global = gtk.Label("VMM Configuration")
        self.label_Global.set_markup('<span color="green" size="18000"><b>VMM Configuration</b></span>')
        self.label_Global.set_justify(gtk.JUSTIFY_CENTER)
        self.box_Global = gtk.HBox()
        self.box_Global.pack_start(self.label_Global, expand=False)

        self.label_vmm_number = gtk.Label("VMM #")
        self.label_vmm_number.set_markup('<span color="green"><b>VMM #</b></span>')
        self.label_vmm_number.set_justify(gtk.JUSTIFY_CENTER)
        self.combo_vmm_number = gtk.combo_box_new_text()
        for ivmm in xrange(8):
            self.combo_vmm_number.append_text(str(ivmm))
        self.combo_vmm_number.append_text("all")
        self.box_vmm_number = gtk.HBox()
        self.box_vmm_number.pack_start(self.label_vmm_number, expand=False)
        self.box_vmm_number.pack_start(self.combo_vmm_number, expand=False)

        self.check_button_SPG = gtk.CheckButton() 
        self.check_button_SPG.connect("toggled", self.glob_callback, registers.SPG)
        self.label_SPG = gtk.Label("Input Charge Polarity")
        self.label_SPG.set_markup('<span color="green"><b>Input Charge Polarity   </b></span>')
        self.label_SPGa = gtk.Label(" spg")   
        self.box_SPG = gtk.HBox()
        self.box_SPG.pack_start(self.label_SPG, expand=False) 
        self.box_SPG.pack_start(self.check_button_SPG, expand=False)
        self.box_SPG.pack_start(self.label_SPGa, expand=False)
            
        self.check_button_SBMX = gtk.CheckButton("")
        self.check_button_SBMX.connect("toggled", self.glob_callback, registers.SBMX)
        self.check_button_SBMX.set_active(0)
        self.label_SBMX = gtk.Label("Route Analog Monitor to PDO Output")
        self.label_SBMX.set_markup('<span color="green"><b>Route Analog Monitor to PDO Output   </b></span>')
        self.label_SBMXa = gtk.Label(" sbmx")
        self.box_SBMX = gtk.HBox()
        self.box_SBMX.pack_start(self.label_SBMX, expand=False)
        self.box_SBMX.pack_start(self.check_button_SBMX, expand=False)
        self.box_SBMX.pack_start(self.label_SBMXa, expand=False)

        self.check_button_SDP = gtk.CheckButton()
        self.check_button_SDP.connect("toggled", self.glob_callback, registers.SDP)
        self.label_SDP = gtk.Label("Disable-at-Peak")
        self.label_SDP.set_markup('<span color="green"><b>Disable-at-Peak   </b></span>')
        self.label_SDPa = gtk.Label(" sdp")
        self.box_SDP = gtk.HBox()
        self.box_SDP.pack_start(self.label_SDP, expand=False)
        self.box_SDP.pack_start(self.check_button_SDP, expand=False)
        self.box_SDP.pack_start(self.label_SDPa, expand=False)

        self.check_button_SBFT = gtk.CheckButton("TDO")
        self.check_button_SBFT.connect("toggled", self.glob_callback, registers.SBFT)
        self.check_button_SBFT.set_active(1)
        self.check_button_SBFP = gtk.CheckButton("PDO")
        self.check_button_SBFP.connect("toggled", self.glob_callback, registers.SBFP)
        self.check_button_SBFP.set_active(1)
        self.check_button_SBFM = gtk.CheckButton("MO")
        self.check_button_SBFM.connect("toggled", self.glob_callback, registers.SBFM)
        self.check_button_SBFM.set_active(1)
        self.label_SBXX = gtk.Label("Analog Output Buffers:")
        self.label_SBXX.set_markup('<span color="green"><b>Analog Output Buffers   </b></span>')
        self.box_SBXX = gtk.HBox()
        self.box_SBXX.pack_start(self.label_SBXX, expand=False)
        self.box_SBXX.pack_start(self.check_button_SBFT, expand=False)
        self.box_SBXX.pack_start(self.check_button_SBFP, expand=False)
        self.box_SBXX.pack_start(self.check_button_SBFM, expand=False)
        
        self.check_button_SLG = gtk.CheckButton() 
        self.check_button_SLG.connect("toggled", self.glob_callback, registers.SLG)
        self.label_SLG = gtk.Label("Leakage Current Disable")
        self.label_SLG.set_markup('<span color="green"><b>Leakage Current Disable   </b></span>')   
        self.label_SLGa = gtk.Label(" slg")
        self.box_SLG = gtk.HBox()
        self.box_SLG.pack_start(self.label_SLG, expand=False) 
        self.box_SLG.pack_start(self.check_button_SLG, expand=False)
        self.box_SLG.pack_start(self.label_SLGa, expand=False)

        self.label_SM = gtk.Label("   Monitor")
        self.label_SM.set_markup('<span color="green"><b>   Monitor   </b></span>')
        self.combo_SM = gtk.combo_box_new_text()
        self.combo_SM.connect("changed", self.glob_SM_value)
        self.combo_SM.append_text("CHN 1")
        self.combo_SM.append_text("CHN 2 | pulser DAC")
        self.combo_SM.append_text("CHN 3 | threshold DAC")
        self.combo_SM.append_text("CHN 4 | band-gap ref")
        self.combo_SM.append_text("CHN 5 | temp")
        for i in range(5, 64):
            self.combo_SM.append_text("CHN " + str(i+1))
        self.combo_SM.set_active(8)

        self.label_SCMX = gtk.Label(" scmx")
        self.label_SCMX.set_markup('<span color="green"><b>SCMX   </b></span>')
        self.check_button_SCMX = gtk.CheckButton()   
        self.check_button_SCMX.connect("toggled", self.glob_callback, registers.SCMX)
        self.check_button_SCMX.set_active(1)
        self.box_SCMX = gtk.HBox()
        self.box_SCMX.pack_start(self.label_SCMX, expand=False)
        self.box_SCMX.pack_start(self.check_button_SCMX, expand=False)
        self.box_SCMX.pack_start(self.label_SM, expand=False) 
        self.box_SCMX.pack_start(self.combo_SM, expand=False)

        self.label_SFA = gtk.Label("ART Enable")
        self.label_SFA.set_markup('<span color="green"><b>ART Enable   </b></span>')    
        self.check_button_SFA = gtk.CheckButton()
        self.check_button_SFA.connect("toggled", self.glob_callback, registers.SFA)
        self.check_button_SFA.set_active(True)
        self.label_SFAa = gtk.Label(" sfa")
        self.label_mode_SFAM = gtk.Label("  Mode    ")
        self.label_mode_SFAM.set_markup('<span color="green"><b>  Mode    </b></span>')
        self.combo_SFAM = gtk.combo_box_new_text()
        self.combo_SFAM.connect("changed", self.glob_callback, registers.SFAM)
        self.combo_SFAM.append_text("timing-at-threshold")      
        self.combo_SFAM.append_text("timing-at-peak")
        self.combo_SFAM.set_active(0)
        self.label_SFAM = gtk.Label(" sfam")
        self.box_SFAM = gtk.HBox()
        self.box_SFAM.pack_start(self.label_SFA, expand=False)
        self.box_SFAM.pack_start(self.check_button_SFA, expand=False)
        self.box_SFAM.pack_start(self.label_SFAa, expand=False)
        self.box_SFAM.pack_start(self.label_mode_SFAM, expand=False)
        self.box_SFAM.pack_start(self.combo_SFAM, expand=False)
        self.box_SFAM.pack_start(self.label_SFAM, expand=False)

        self.label_Var_ST = gtk.Label("Peaking Time")
        self.label_Var_ST.set_markup('<span color="green"><b>Peaking Time   </b></span>')
        self.combo_ST = gtk.combo_box_new_text()
        self.combo_ST.connect("changed",self.glob_ST_value)
        self.combo_ST.append_text("200 ns")
        self.combo_ST.append_text("100 ns")
        self.combo_ST.append_text("50 ns")
        self.combo_ST.append_text("25 ns")
        self.combo_ST.set_active(0)
        self.label_ST = gtk.Label(" st")
        self.box_ST = gtk.HBox()
        self.box_ST.pack_start(self.label_Var_ST, expand=False)
        self.box_ST.pack_start(self.combo_ST, expand=False)
        self.box_ST.pack_start(self.label_ST, expand=False)

        self.check_button_SFM = gtk.CheckButton()
        self.label_SFM = gtk.Label("SFM")
        self.label_SFM.set_markup('<span color="green"><b>SFM   </b></span>')   
        self.check_button_SFM.connect("toggled", self.glob_callback, registers.SFM)
        self.check_button_SFM.set_active(1)
        self.label_SFMb = gtk.Label("  Doubles the Leakage Current")
        self.label_SFMb.set_markup('<span color="green"><b>  (Doubles the Leakage Current)</b></span>')        
        self.box_SFM = gtk.HBox()
        self.box_SFM.pack_start(self.label_SFM, expand=False) 
        self.box_SFM.pack_start(self.check_button_SFM, expand=False)
        self.box_SFM.pack_start(self.label_SFMb, expand=False)

        self.label_Var_SG = gtk.Label("Gain")
        self.label_Var_SG.set_markup('<span color="green"><b>Gain   </b></span>')
        self.combo_SG = gtk.combo_box_new_text()
        self.combo_SG.connect("changed",self.glob_SG_value)
        self.combo_SG.append_text("0.5 (000)")     
        self.combo_SG.append_text("1 (001)")
        self.combo_SG.append_text("3 (010)")
        self.combo_SG.append_text("4.5 (011)")
        self.combo_SG.append_text("6 (100)")
        self.combo_SG.append_text("9 (101)")
        self.combo_SG.append_text("12 (110)")
        self.combo_SG.append_text("16 (111)")
        self.combo_SG.set_active(5)
        self.label_SG = gtk.Label(" (mV/fC)    sg")
        self.box_SG = gtk.HBox()
        self.box_SG.pack_start(self.label_Var_SG, expand=False)
        self.box_SG.pack_start(self.combo_SG, expand=False)
        self.box_SG.pack_start(self.label_SG, expand=False)

        self.check_button_SNG = gtk.CheckButton() 
        self.label_SNG = gtk.Label("Neighbor Triggering")
        self.label_SNG.set_markup('<span color="green"><b>Neighbor Triggering   </b></span>')    
        self.check_button_SNG.connect("toggled", self.glob_callback, registers.SNG)
        self.label_SNGa = gtk.Label(" sng")
        self.box_SNG = gtk.HBox()
        self.box_SNG.pack_start(self.label_SNG, expand=False) 
        self.box_SNG.pack_start(self.check_button_SNG,expand=False)
        self.box_SNG.pack_start(self.label_SNGa, expand=False) 

        self.label_STTT = gtk.Label("Timing Outputs")
        self.label_STTT.set_markup('<span color="green"><b>Timing Outputs </b></span>')
        self.check_button_STTT = gtk.CheckButton()
        self.check_button_STTT.connect("toggled", self.glob_callback, registers.STTT)
        self.label_STTTa = gtk.Label(" sttt")
        self.label_mode_STOT = gtk.Label("  Mode    ")
        self.label_mode_STOT.set_markup('<span color="green"><b>  Mode  </b></span>')
        self.combo_STOT = gtk.combo_box_new_text()
        self.combo_STOT.connect("changed", self.glob_callback, registers.STOT)
        self.combo_STOT.append_text("threshold-to-peak")
        self.combo_STOT.append_text("time-over-threshold")
        self.combo_STOT.set_active(0)        
        self.label_STOT = gtk.Label(" stot")
        self.box_STXX = gtk.HBox()
        self.box_STXX.pack_start(self.label_STTT, expand=False)                
        self.box_STXX.pack_start(self.check_button_STTT, expand=False)
        self.box_STXX.pack_start(self.label_STTTa, expand=False)
        self.box_STXX.pack_start(self.label_mode_STOT, expand=False)
        self.box_STXX.pack_start(self.combo_STOT, expand=False)
        self.box_STXX.pack_start(self.label_STOT, expand=False)

        self.label_SSH = gtk.Label("Sub-Hysteresis\nDiscrimination")    
        self.label_SSH.set_markup('<span color="green"><b>Sub-Hysteresis   \nDiscrimination</b></span>')
        self.check_button_SSH = gtk.CheckButton()
        self.check_button_SSH.connect("toggled", self.glob_callback, registers.SSH)
        self.label_SSHa = gtk.Label(" ssh")
        self.box_SSH = gtk.HBox()
        self.box_SSH.pack_start(self.label_SSH, expand=False)        
        self.box_SSH.pack_start(self.check_button_SSH, expand=False)
        self.box_SSH.pack_start(self.label_SSHa, expand=False)

        self.label_STPP = gtk.Label("Timing Outputs Control 2")    
        self.label_STPP.set_markup('<span color="green"><b>Timing Outputs Control 2   </b></span>')
        self.check_button_STPP = gtk.CheckButton()
        self.check_button_STPP.connect("toggled", self.glob_callback, registers.STPP)
        self.label_STPPa = gtk.Label(" stpp")
        self.box_STPP = gtk.HBox()
        self.box_STPP.pack_start(self.label_STPP, expand=False)        
        self.box_STPP.pack_start(self.check_button_STPP, expand=False)
        self.box_STPP.pack_start(self.label_STPPa, expand=False)

        self.label_Var_STC = gtk.Label("TAC Slope")
        self.label_Var_STC.set_markup('<span color="green"><b>TAC Slope   </b></span>')              
        self.combo_STC = gtk.combo_box_new_text()
        self.combo_STC.connect("changed", self.glob_STC_value)
        self.combo_STC.append_text("125 ns (00)")        
        self.combo_STC.append_text("250 ns (01)")
        self.combo_STC.append_text("500 ns (10)")
        self.combo_STC.append_text("1000 ns (11)")
        self.combo_STC.set_active(2)
        self.label_STC = gtk.Label(" stc")
        self.box_STC = gtk.HBox()
        self.box_STC.pack_start(self.label_Var_STC, expand=False)
        self.box_STC.pack_start(self.combo_STC, expand=False)
        self.box_STC.pack_start(self.label_STC, expand=False)

        self.label_Var_SDT = gtk.Label("Threshold DAC")
        self.label_Var_SDT.set_markup('<span color="green"><b>Threshold DAC   </b></span>')
        self.entry_SDT = gtk.Entry(max=4)
        self.entry_SDT.set_text("300")
        self.entry_SDT.connect("focus-out-event", self.glob_SDT_entry)
        self.entry_SDT.connect("activate", self.glob_SDT_entry, self.entry_SDT)

        self.label_SDT = gtk.Label()
        self.box_SDT = gtk.HBox()
        self.box_SDT.pack_start(self.label_Var_SDT, expand=False)
        self.box_SDT.pack_start(self.entry_SDT, expand=False)
        #self.box_SDT.pack_start(self.combo_SDT)
        self.box_SDT.pack_start(self.label_SDT, expand=False)
        #self.box_SDT.pack_start(self.label_Var_SDTb, expand=False)

        self.label_Var_SDP_ = gtk.Label("Test Pulse DAC")
        self.label_Var_SDP_.set_markup('<span color="green"><b>Test Pulse DAC   </b></span>')
        self.entry_SDP_ = gtk.Entry(max=4)
        self.entry_SDP_.set_text("300")
        self.entry_SDP_.connect("focus-out-event", self.glob_SDP_entry ) #,self.entry_SDP_
        self.entry_SDP_.connect("activate", self.glob_SDP_entry, self.entry_SDP_)

        self.label_SDP_ = gtk.Label()
        self.box_SDP_ = gtk.HBox()
        self.box_SDP_.pack_start(self.label_Var_SDP_,expand=False)
        self.box_SDP_.pack_start(self.entry_SDP_,expand=False)
        self.box_SDP_.pack_start(self.label_SDP_,expand=False)

        self.label_variable1 = gtk.Label("  \n   ")
        self.label_variable2 = gtk.Label("  \n   ")
        self.label_variable3 = gtk.Label("  \n   ")
        self.label_variable4 = gtk.Label("  \n   ") 
        self.label_variable5 = gtk.Label("   ")
        self.label_variable6 = gtk.Label("Values for Threshold and Test Pulse :") 
        self.label_variable6.set_markup('<span color="purple"><b>Values for Threshold and Test Pulse :</b></span>') 
        self.label_variable7 = gtk.Label("  \n  ")
        self.label_variable9 = gtk.Label("  \n  ") 
        self.label_variable10 = gtk.Label("  0 <= x <= 1023")
        self.label_variable11 = gtk.Label(" ")
        self.label_variable12 = gtk.Label("to Set the Values for SDT and SDP_")
        self.label_variable12.set_markup('<span color="purple">to <b>Set</b> the Values for <b>SDT</b> and <b>SDP_</b></span>')
        self.box_SDP_SDT = gtk.HBox()
        self.box_SDP_SDT.pack_start(self.label_variable6,expand=False)
        self.box_SDP_SDT.pack_start(self.label_variable10,expand=False)

        self.label_Var_SC10b = gtk.Label("10-bit Conversion Time")
        self.label_Var_SC10b.set_markup('<span color="green"><b>10-bit Conversion Time   </b></span>')
        self.combo_SC10b = gtk.combo_box_new_text()
        self.combo_SC10b.connect("changed", self.glob_SC10b_value)
        self.combo_SC10b.append_text("0 ns (00)")
        self.combo_SC10b.append_text("1 ns (10)")
        self.combo_SC10b.append_text("2 ns (01)")
        self.combo_SC10b.append_text("3 ns (11)")
        self.combo_SC10b.set_active(0)
        self.label_SC10b = gtk.Label(" sc10b")
        self.box_SC10b = gtk.HBox()
        self.box_SC10b.pack_start(self.label_Var_SC10b, expand=False)
        self.box_SC10b.pack_start(self.combo_SC10b, expand=False)
        self.box_SC10b.pack_start(self.label_SC10b, expand=False)

        self.label_Var_SC8b = gtk.Label("8-bit Conversion Time")
        self.label_Var_SC8b.set_markup('<span color="green"><b>8-bit Conversion Time   </b></span>')
        self.combo_SC8b = gtk.combo_box_new_text()
        self.combo_SC8b.connect("changed", self.glob_SC8b_value)
        self.combo_SC8b.append_text("0 ns (00)")
        self.combo_SC8b.append_text("1 ns (10)")
        self.combo_SC8b.append_text("2 ns (01)")
        self.combo_SC8b.append_text("3 ns (11)")
        self.combo_SC8b.set_active(0)
        self.label_SC8b = gtk.Label(" sc8b")
        self.box_SC8b = gtk.HBox()
        self.box_SC8b.pack_start(self.label_Var_SC8b, expand=False)
        self.box_SC8b.pack_start(self.combo_SC8b, expand=False)
        self.box_SC8b.pack_start(self.label_SC8b, expand=False)

        self.label_Var_SC6b = gtk.Label("6-bit Conversion Time")
        self.label_Var_SC6b.set_markup('<span color="green"><b>6-bit Conversion Time   </b></span>')
        self.combo_SC6b = gtk.combo_box_new_text()
        self.combo_SC6b.connect("changed", self.glob_SC6b_value)
        self.combo_SC6b.append_text("0 ns (000)")
        self.combo_SC6b.append_text("1 ns (100)")
        self.combo_SC6b.append_text("2 ns (010)")
        self.combo_SC6b.append_text("3 ns (110)")
        self.combo_SC6b.append_text("4 ns (001)")
        self.combo_SC6b.append_text("5 ns (101)")
        self.combo_SC6b.append_text("6 ns (011)")
        self.combo_SC6b.append_text("7 ns (111)")
        self.combo_SC6b.set_active(0)
        self.label_Var_SC6ba = gtk.Label(" sc6b")
        self.box_SC6b = gtk.HBox()
        self.box_SC6b.pack_start(self.label_Var_SC6b, expand=False)
        self.box_SC6b.pack_start(self.combo_SC6b, expand=False)
        self.box_SC6b.pack_start(self.label_Var_SC6ba, expand=False)

        self.label_S6b = gtk.Label("6-bit ADC Enable")
        self.label_S6b.set_markup('<span color="green"><b>6-bit ADC Enable   </b></span>')
        self.check_button_S6b = gtk.CheckButton()   
        self.check_button_S6b.connect("toggled", self.glob_callback, registers.S6b)
        self.check_button_S6b.set_active(False)
        self.label_S6ba = gtk.Label("Disables 8 & 10 bit ADC")
        self.label_S6ba.set_markup('<span color="green"><b>  (Disables 8 &amp; 10 bit ADC)</b></span>')
        self.label_S6bb = gtk.Label(" s6b")
        self.box_S6b = gtk.HBox()
        self.box_S6b.pack_start(self.label_S6b, expand=False)
        self.box_S6b.pack_start(self.check_button_S6b, expand=False)
        self.box_S6b.pack_start(self.label_S6ba, expand=False)
        self.box_S6b.pack_start(self.label_S6bb, expand=False)

        self.label_Var_S8b = gtk.Label("8-bit ADC Mode")
        self.label_Var_S8b.set_markup('<span color="green"><b>8-bit ADC Mode   </b></span>')
        self.combo_S8b = gtk.CheckButton()
        self.combo_S8b.connect("toggled", self.glob_callback, registers.S8b)
        self.combo_S8b.set_active(1)
        self.label_Var_S8ba = gtk.Label(" s8b")
        self.box_S8b = gtk.HBox()
        self.box_S8b.pack_start(self.label_Var_S8b, expand=False)
        self.box_S8b.pack_start(self.combo_S8b, expand=False)
        self.box_S8b.pack_start(self.label_Var_S8ba, expand=False)

        self.label_Var_SPDC = gtk.Label("ADCs Enable")
        self.label_Var_SPDC.set_markup('<span color="green"><b>ADCs Enable   </b></span>')
        self.button_SPDC = gtk.CheckButton()
        self.button_SPDC.connect("toggled", self.glob_callback, registers.SPDC)
        self.button_SPDC.set_active(1)
        self.label_Var_SPDCa = gtk.Label(" spdc")
        self.box_SPDC = gtk.HBox()
        self.box_SPDC.pack_start(self.label_Var_SPDC, expand=False)
        self.box_SPDC.pack_start(self.button_SPDC, expand=False)
        self.box_SPDC.pack_start(self.label_Var_SPDCa, expand=False)

        self.label_SDCKS = gtk.Label("Dual Clock Edge\nSerialized Data Enable\n")    
        self.label_SDCKS.set_markup('<span color="green"><b>Dual Clock Edge\nSerialized Data Enable\n   </b></span>')
        self.check_button_SDCKS = gtk.CheckButton()
        self.check_button_SDCKS.connect("toggled", self.glob_callback, registers.SDCKS)
        self.label_SDCKSa = gtk.Label(" sdcks")
        self.box_SDCKS = gtk.HBox()
        self.box_SDCKS.pack_start(self.label_SDCKS, expand=False)        
        self.box_SDCKS.pack_start(self.check_button_SDCKS, expand=False)
        self.box_SDCKS.pack_start(self.label_SDCKSa, expand=False)

        self.label_SDCKA = gtk.Label("Dual Clock Edge\nSerialized ART Enable\n")    
        self.label_SDCKA.set_markup('<span color="green"><b>Dual Clock Edge\nSerialized ART Enable\n   </b></span>')
        self.check_button_SDCKA = gtk.CheckButton()
        self.check_button_SDCKA.connect("toggled", self.glob_callback, registers.SDCKA)
        self.label_SDCKAa = gtk.Label(" sdcka")
        self.box_SDCKA = gtk.HBox()
        self.box_SDCKA.pack_start(self.label_SDCKA, expand=False)        
        self.box_SDCKA.pack_start(self.check_button_SDCKA, expand=False)
        self.box_SDCKA.pack_start(self.label_SDCKAa, expand=False)

        self.label_SDCK6b = gtk.Label("Dual Clock Edge\nSerialized 6-bit Enable\n")    
        self.label_SDCK6b.set_markup('<span color="green"><b>Dual Clock Edge\nSerialized 6-bit Enable\n    </b></span>')
        self.check_button_SDCK6b = gtk.CheckButton()
        self.check_button_SDCK6b.connect("toggled", self.glob_callback, registers.SDCK6b)
        self.label_SDCK6ba = gtk.Label(" sdck6b")
        self.box_SDCK6b = gtk.HBox()
        self.box_SDCK6b.pack_start(self.label_SDCK6b, expand=False)        
        self.box_SDCK6b.pack_start(self.check_button_SDCK6b, expand=False)
        self.box_SDCK6b.pack_start(self.label_SDCK6ba, expand=False)

        self.label_SDRV = gtk.Label("Tristates Analog Outputs")    
        self.label_SDRV.set_markup('<span color="green"><b>Tristates Analog Outputs   </b></span>')
        self.check_button_SDRV = gtk.CheckButton()
        self.check_button_SDRV.connect("toggled", self.glob_callback, registers.SDRV)
        self.check_button_SDRV.set_active(0)
        self.label_SDRVa = gtk.Label(" sdrv")
        self.box_SDRV = gtk.HBox()
        self.box_SDRV.pack_start(self.label_SDRV, expand=False)        
        self.box_SDRV.pack_start(self.check_button_SDRV, expand=False)
        self.box_SDRV.pack_start(self.label_SDRVa, expand=False)

        self.box_var_labels = gtk.VBox()
        self.box_var_labels.set_border_width(10)
        self.box_var_labels.pack_start(self.label_variable1)
        self.box_var_labels.pack_start(self.label_variable2)
        self.box_var_labels.pack_start(self.label_variable3)
        self.frame_qs = gtk.Frame()
        self.frame_qs.set_shadow_type(gtk.SHADOW_OUT)
        self.frame_qs.set_label("QUICK SET")
        self.frame_qs.set_label_align(0.5,0.0)
        self.box_quick_set = gtk.VBox(homogeneous=False,spacing=0)
        self.box_quick_set.set_border_width(20)
        self.qs_label = gtk.Label("QUICK SET")
        self.qs_label.set_markup('<span color="green"><b>Tristates Analog Outputs   </b></span>')
        self.box_quick_set.pack_start(self.qs_table)
        #self.box_quick_set.pack_end(self.button_quick_set)                
        self.frame_qs.add(self.box_quick_set)

        self.label_But_Space6 = gtk.Label(" ")
        self.label_But_Space7 = gtk.Label(" ")

        self.box_variables = gtk.VBox()
        self.box_variables.set_border_width(5)

        self.box_variables.pack_start(self.box_Global, expand=False)
        self.box_variables.pack_start(self.box_vmm_number, expand=False)
        self.box_variables.pack_start(self.label_But_Space6, expand=False)
        self.box_variables.pack_start(self.label_But_Space7, expand=False)
        self.box_variables.pack_start(self.box_SPG, expand=False)
        self.box_variables.pack_start(self.box_SDP, expand=False)
        self.box_variables.pack_start(self.box_SBMX, expand=False)
        self.box_variables.pack_start(self.box_SBXX, expand=False)
        self.box_variables.pack_start(self.box_SLG, expand=False)
        self.box_variables.pack_start(self.box_SCMX, expand=False)
        self.box_variables.pack_start(self.box_SFAM, expand=False)
        self.box_variables.pack_start(self.box_ST, expand=False)
        self.box_variables.pack_start(self.box_SFM, expand=False)

        self.box_variables.pack_start(self.box_SG, expand=False)
        self.box_variables.pack_start(self.box_SNG, expand=False)
        self.box_variables.pack_start(self.box_STXX, expand=False)

        self.box_variables.pack_start(self.box_SSH, expand=False)
        self.box_variables.pack_start(self.box_STC, expand=False)

        self.box_variables.pack_start(self.box_SC10b, expand=False)
        self.box_variables.pack_start(self.box_S8b, expand=False)
        self.box_variables.pack_start(self.box_SC8b, expand=False)
        self.box_variables.pack_start(self.box_S6b, expand=False)
        self.box_variables.pack_start(self.box_SC6b, expand=False)
        self.box_variables.pack_start(self.box_SPDC, expand=False)
        
        self.box_variables.pack_start(self.box_SDCKS, expand=False)
        self.box_variables.pack_start(self.box_SDCKA, expand=False)
        self.box_variables.pack_start(self.box_SDCK6b, expand=False)
        self.box_variables.pack_start(self.box_SDRV, expand=False)
        self.box_variables.pack_start(self.box_STPP, expand=False)

        self.box_variables.pack_start(self.label_variable5,expand=False)
        self.box_variables.pack_start(self.label_variable11,expand=False)
        self.box_variables.pack_start(self.box_SDT,expand=False)
        self.box_variables.pack_start(self.box_SDP_,expand=False)
        self.box_variables.pack_start(self.box_SDP_SDT,expand=False)
        #self.box_variables.pack_start(self.label_variable12,expand=False)
        self.box_variables.pack_start(self.label_variable9)
        self.box_variables.pack_end(self.frame_qs,expand=False) 

        self.frame_variables = gtk.Frame()
        self.frame_variables.set_border_width(4)
        self.frame_variables.set_shadow_type(gtk.SHADOW_IN)
        self.frame_variables.add(self.box_variables)
        # self.frame_variables.set_size_request(300, -1)

        self.box_all_variables = gtk.HBox()
        self.box_all_variables.pack_start(self.frame_variables)

        ################### CHANNELS FRAMES #############
        
        self.frame_channels = gtk.Frame()
        self.frame_channels.set_border_width(4)
        self.frame_channels.set_shadow_type(gtk.SHADOW_IN)

        self.box_channels_steer = gtk.VBox(homogeneous=False, spacing=0)
        self.box_channels_rows  = gtk.VBox(homogeneous=True,  spacing=0)

        for ch_num in range(64):
            self.box_channels_rows.pack_start(self.chan_list[ch_num].channel_box)

        self.box_channels_steer.pack_start(self.box_channels,      expand=False)
        self.box_channels_steer.pack_start(self.box_chan_labels_a, expand=False)
        self.box_channels_steer.pack_start(self.box_channels_rows, expand=False)
        self.frame_channels.add(self.box_channels_steer)

        self.box_all_channels = gtk.HBox()
        self.box_all_channels.pack_start(self.frame_channels)


