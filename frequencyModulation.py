#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Frequencymodulation
# GNU Radio version: 3.7.13.5
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import wx


class frequencyModulation(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Frequencymodulation")
        _icon_path = "C:\Program Files\GNURadio-3.7\share\icons\hicolor\scalable/apps\gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 360000
        self.vol = vol = .2
        self.vco_sens = vco_sens = 753982.2369

        self.taps_up = taps_up = firdes.low_pass(1.0, samp_rate, 7500, 500, firdes.WIN_HAMMING, 6.76)

        self.source_rate = source_rate = 48000
        self.source = source = 0
        self.mode = mode = 0
        self.level = level = .1
        self.freq = freq = 0

        ##################################################
        # Blocks
        ##################################################
        _vol_sizer = wx.BoxSizer(wx.VERTICAL)
        self._vol_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_vol_sizer,
        	value=self.vol,
        	callback=self.set_vol,
        	label='Volume',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._vol_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_vol_sizer,
        	value=self.vol,
        	callback=self.set_vol,
        	minimum=0,
        	maximum=1,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_vol_sizer, 0, 30, 1, 10)
        self.tabs = self.tabs = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.tabs.AddPage(grc_wxgui.Panel(self.tabs), "source")
        self.tabs.AddPage(grc_wxgui.Panel(self.tabs), "trum")
        self.tabs.AddPage(grc_wxgui.Panel(self.tabs), "Demod")
        self.Add(self.tabs)
        self._source_chooser = forms.radio_buttons(
        	parent=self.GetWin(),
        	value=self.source,
        	callback=self.set_source,
        	label='Source',
        	choices=[0,1],
        	labels=['Tone','Audio'],
        	style=wx.RA_HORIZONTAL,
        )
        self.GridAdd(self._source_chooser, 0, 0, 1, 10)
        _level_sizer = wx.BoxSizer(wx.VERTICAL)
        self._level_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_level_sizer,
        	value=self.level,
        	callback=self.set_level,
        	label='Level',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._level_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_level_sizer,
        	value=self.level,
        	callback=self.set_level,
        	minimum=0,
        	maximum=1,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_level_sizer, 0, 10, 1, 10)
        _freq_sizer = wx.BoxSizer(wx.VERTICAL)
        self._freq_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	label='Frequency',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._freq_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	minimum=0,
        	maximum=5000,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_freq_sizer, 0, 20, 1, 10)
        self.wxgui_scopesink2_2 = scopesink2.scope_sink_f(
        	self.tabs.GetPage(1).GetWin(),
        	title=' FM Signal',
        	sample_rate=360000,
        	v_scale=0.5,
        	v_offset=0,
        	t_scale=0.005,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label='Amplitude',
        )
        self.tabs.GetPage(1).Add(self.wxgui_scopesink2_2.win)
        self.wxgui_scopesink2_1 = scopesink2.scope_sink_f(
        	self.tabs.GetPage(1).GetWin(),
        	title='Signal Modulada',
        	sample_rate=samp_rate,
        	v_scale=0.05,
        	v_offset=1,
        	t_scale=0.01,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label='Amplitude',
        )
        self.tabs.GetPage(1).Add(self.wxgui_scopesink2_1.win)
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
        	self.tabs.GetPage(0).GetWin(),
        	title='Banda Base de Audio',
        	sample_rate=source_rate,
        	v_scale=0.5,
        	v_offset=0,
        	t_scale=0.005,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label='Amplitude',
        )
        self.tabs.GetPage(0).Add(self.wxgui_scopesink2_0.win)
        self.wxgui_fftsink2_1 = fftsink2.fft_sink_f(
        	self.tabs.GetPage(2).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=2048,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='Salida espectro FM',
        	peak_hold=False,
        )
        self.tabs.GetPage(2).Add(self.wxgui_fftsink2_1.win)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_f(
        	self.tabs.GetPage(2).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=24000,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='Demodulador FM',
        	peak_hold=False,
        )
        self.tabs.GetPage(2).Add(self.wxgui_fftsink2_0.win)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=15,
                decimation=2,
                taps=(taps_up),
                fractional_bw=None,
        )
        self._mode_chooser = forms.radio_buttons(
        	parent=self.GetWin(),
        	value=self.mode,
        	callback=self.set_mode,
        	label='Mode',
        	choices=[0,1],
        	labels=['Norm','Cal'],
        	style=wx.RA_HORIZONTAL,
        )
        self.GridAdd(self._mode_chooser, 0, 40, 4, 10)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('C:\\Users\\ALEX GUAILLA\\Desktop\\GABYTA\\icon.wav', True)
        self.blocks_vco_f_0 = blocks.vco_f(360000, 753982, 1)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((vol, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((level*5, ))
        self.blocks_integrate_xx_0 = blocks.integrate_ff(1, 1)
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((1, ))
        self.blks2_selector_1 = grc_blks2.selector(
        	item_size=gr.sizeof_float*1,
        	num_inputs=2,
        	num_outputs=1,
        	input_index=0,
        	output_index=0,
        )
        self.blks2_selector_0 = grc_blks2.selector(
        	item_size=gr.sizeof_float*1,
        	num_inputs=2,
        	num_outputs=1,
        	input_index=source,
        	output_index=0,
        )
        self.band_pass_filter_0 = filter.fir_filter_fcc(3, firdes.complex_band_pass(
        	1, samp_rate, 100000, 140000, 2000, firdes.WIN_HAMMING, 6.76))
        self.audio_sink_0 = audio.sink(24000, '', True)
        self.analog_sig_source_x_1 = analog.sig_source_f(source_rate, analog.GR_COS_WAVE, freq, level, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_CONST_WAVE, 1000, level, 1)
        self.analog_fm_demod_cf_0 = analog.fm_demod_cf(
        	channel_rate=120000,
        	audio_decim=5,
        	deviation=10000,
        	audio_pass=10000,
        	audio_stop=11000,
        	gain=1.0,
        	tau=0,
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fm_demod_cf_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blks2_selector_1, 1))
        self.connect((self.analog_sig_source_x_1, 0), (self.blks2_selector_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.analog_fm_demod_cf_0, 0))
        self.connect((self.blks2_selector_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blks2_selector_0, 0), (self.wxgui_scopesink2_0, 0))
        self.connect((self.blks2_selector_1, 0), (self.blocks_vco_f_0, 0))
        self.connect((self.blks2_selector_1, 0), (self.wxgui_scopesink2_1, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.blks2_selector_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blks2_selector_0, 1))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.wxgui_fftsink2_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_vco_f_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_vco_f_0, 0), (self.wxgui_fftsink2_1, 0))
        self.connect((self.blocks_vco_f_0, 0), (self.wxgui_scopesink2_2, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_throttle_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_scopesink2_1.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_1.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.samp_rate, 100000, 140000, 2000, firdes.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_vol(self):
        return self.vol

    def set_vol(self, vol):
        self.vol = vol
        self._vol_slider.set_value(self.vol)
        self._vol_text_box.set_value(self.vol)
        self.blocks_multiply_const_vxx_1.set_k((self.vol, ))

    def get_vco_sens(self):
        return self.vco_sens

    def set_vco_sens(self, vco_sens):
        self.vco_sens = vco_sens

    def get_taps_up(self):
        return self.taps_up

    def set_taps_up(self, taps_up):
        self.taps_up = taps_up
        self.rational_resampler_xxx_0.set_taps((self.taps_up))

    def get_source_rate(self):
        return self.source_rate

    def set_source_rate(self, source_rate):
        self.source_rate = source_rate
        self.wxgui_scopesink2_0.set_sample_rate(self.source_rate)
        self.analog_sig_source_x_1.set_sampling_freq(self.source_rate)

    def get_source(self):
        return self.source

    def set_source(self, source):
        self.source = source
        self._source_chooser.set_value(self.source)
        self.blks2_selector_0.set_input_index(int(self.source))

    def get_mode(self):
        return self.mode

    def set_mode(self, mode):
        self.mode = mode
        self._mode_chooser.set_value(self.mode)

    def get_level(self):
        return self.level

    def set_level(self, level):
        self.level = level
        self._level_slider.set_value(self.level)
        self._level_text_box.set_value(self.level)
        self.blocks_multiply_const_vxx_0.set_k((self.level*5, ))
        self.analog_sig_source_x_1.set_amplitude(self.level)
        self.analog_sig_source_x_0.set_amplitude(self.level)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self._freq_slider.set_value(self.freq)
        self._freq_text_box.set_value(self.freq)
        self.analog_sig_source_x_1.set_frequency(self.freq)


def main(top_block_cls=frequencyModulation, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
