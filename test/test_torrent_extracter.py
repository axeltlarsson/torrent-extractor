#!/usr/bin/python3
# Run the tests from the project root (torrent_extracter) with: python3 -m unittest discover --pattern=test_*

import unittest, subprocess, os


class TorrentExtracterTest(unittest.TestCase):
	""" Contains test cases for torrent_extracter.py """
	
	def setUp(self):
		self.errors = [] # collects errors
		
		self.path = "/media/public/Nedladdning/klart/"
		self.downloads = []
		self.downloads.append(("A.FLAWL3SS.M3GA.PACK.1080P.X264 {INFERNO}", 'films/American Psycho/American.Psycho.2000.1080p.DTS.dxva.x264.FLAWL3SS.mkv'))
		self.downloads.append(('A.Lonely.Place.to.Die.2011.1080p.BluRay.DTS-HD.x264-BARC0DE', 'films/A Lonely Place to Die/A.Lonely.Place.to.Die.2011.1080p.BluRay.DTS-HD.x264-BARC0DE.mkv'))
		self.downloads.append(('Austin.Powers.Boxset.TorrentLeech.1080p', 'films/Austin Powers in Goldmember/tl-apig.mkv', 'films/Austin Powers International Man Of Mystery/Austin.Powers.International.Man.Of.Mystery.1080p-iKA.mkv', 'films/Austin Powers The Spy Who Shagged Me/tl-aptswsm.mkv'))
		self.downloads.append(('Bourne.Trilogy.COMPLETE.1080p.x264-TL', 'films/The Bourne Identity/tl-tbi.mkv', 'films/The Bourne Supremacy/tl-tbs.mkv', 'films/The Bourne Ultimatum/The.Bourne.Ultimatum.2007.1080p.HDVD.DTS.x264-hV.mkv'))
		self.downloads.append(('Divergent.2014.720p.BluRay.DD5.1.x264-HiDt', 'films/Divergent/Divergent.2014.720p.BluRay.DD5.1.x264-HiDt.mkv'))
		self.downloads.append(('Good.Will.Hunting.1997.1080p.15th.Anniversary.Edition.BluRay.DTS-HD.x264-BARC0DE', 'films/Good Will Hunting/Good.Will.Hunting.1997.1080p.15th.Anniversary.Edition.BluRay.DTS-HD.x264-BARC0DE.mkv'))
		#self.downloads.append(('James bond 1080p.BluRay.x264 BIG PACK -TL', 'James bond')) # The World is not enough saknar part04.rar, "James.Bond.007.Quantum.of.Solace.1080p.BluRay.x264-REFiNED" känns inte igen i regex
		#self.downloads.append('John Denver - Greatest Hits [1973]  FLAC')
		#self.downloads.append('John Denver - The Very Best Of John Denver')
		#self.downloads.append('King Arthur - soundtrack')
		#self.downloads.append('Masters.of.Sex.S02E07.720p.HDTV.x264-IMMERSE')
		#self.downloads.append('Microsoft Office ProPlus 2013 VL x64 en-US Jun2013')
		#self.downloads.append('Midsomer.Murders.S13E02.WS.PDTV.XviD-RiVER [NO-RAR] - [ www.torrentday.com ]')
		#self.downloads.append('Rome.S01.1080p.Bluray.x264-H@M')
		#self.downloads.append('Rome.S02.1080p.Bluray.x264-H@M')
		#self.downloads.append('Star Wars The Complete Saga 1977-2005 1080p Blu-ray Remux AVC DTS-HD MA 6.1 - KRaLiMaRKo')
		#self.downloads.append('Tales of Dunk and Egg')
		# Inga LOTR fungerar - eftersom de inte innehåller årtalet.
		#self.downloads.append('The.Lord.of.The.Rings.Extended.Edition.Trilogy.1080p.Blu-Ray.DTSMA.dxva.x264-FLAWL3SS')
		self.downloads.append(('Game.of.Thrones.S04E07.1080p.HDTV.AC3-REsuRRecTioN.mkv', 'tv_series/Game of Thrones/Season 4/Game.of.Thrones.S04E07.1080p.HDTV.AC3-REsuRRecTioN.mkv'))
		
		self.nonce = []

	def tearDown(self):
		self.assertEqual([], self.errors) # test that we have no errors

	# Tests that files have actually been copied/extracted as they are meant
	#@unittest.skip("lf")
	def test_copying(self):
		for download in self.downloads:
			cmd = r'python3 ../torrent_extracter_runner.py -t /media/axel/test/tv_series -f /media/axel/test/films "' + self.path + download[0] + '"'
			output = subprocess.getoutput(cmd)
			print(output)
			for i in range(1, len(download) - 1):
				try:
					self.assertTrue(os.path.exists(os.path.join('/media/axel/test', download[i])))
				except AssertionError as e:
					self.errors.append(os.path.join('/media/axel/test', download[i]) + " did not exist")

if __name__ == '__main__':
    unittest.main()