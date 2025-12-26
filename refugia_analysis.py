#!/usr/bin/env python3
"""
Refugia Linguistic Analysis Script
===================================
Statistical analysis of phonemic and grammatical feature distributions
in hypothesized linguistic refugia.

This script:
1. Parses WALS XML data for multiple features
2. Classifies languages into refugia regions
3. Calculates baseline and enrichment statistics
4. Computes Moran's I spatial autocorrelation
5. Performs permutation tests for robustness
6. Generates publication-ready tables

Author: Yesid Castro
Date: 25 December 2025
"""

import xml.etree.ElementTree as ET
import math
import random
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, NamedTuple

# =============================================================================
# DATA STRUCTURES
# =============================================================================

class Language(NamedTuple):
    """Represents a single language data point."""
    code: str
    name: str
    latitude: float
    longitude: float
    value: int
    description: str

class FeatureData(NamedTuple):
    """Represents a complete WALS feature dataset."""
    feature_id: str
    feature_name: str
    languages: List[Language]

# =============================================================================
# WALS DATA
# =============================================================================


WALS_1A_CONSONANTS = """
<feature number="1A" base_url="https://wals.info/" name="Consonant Inventories">
<description>
<url>https://wals.info/feature/1A.xml</url>
<timestamp>2024-10-18T11:59:12.029308+02:00</timestamp>
</description>
<v numeric="1" description="Small" icon_id="c0000dd" icon_url="https://wals.info/clld-static/icons/c0000dd.png" zindex="0">
<l c="ach" n="Aché" lng="-55.1666666667" lat="-25.25"/>
<l c="ain" n="Ainu" lng="143.0" lat="43.0"/>
<l c="akw" n="Akawaio" lng="-59.5" lat="6.0"/>
<l c="abm" n="Alabama" lng="-87.4166666667" lat="32.3333333333"/>
<l c="amc" n="Amahuaca" lng="-72.5" lat="-10.5"/>
<l c="adk" n="Andoke" lng="-72.0" lat="-0.666666666667"/>
<l c="ant" n="Angaataha" lng="146.25" lat="-7.21666666667"/>
<l c="ao" n="Ao" lng="94.6666666667" lat="26.5833333333"/>
<l c="api" n="Apinayé" lng="-48.0" lat="-5.5"/>
<l c="apu" n="Apurinã" lng="-67.0" lat="-9.0"/>
<l c="arb" n="Arabela" lng="-75.1666666667" lat="-2.0"/>
<l c="asm" n="Asmat" lng="138.5" lat="-5.5"/>
<l c="awp" n="Awa Pit" lng="-78.25" lat="1.5"/>
<l c="byu" n="Bandjalang (Yugumbir)" lng="153.0" lat="-27.9166666667"/>
<l c="brr" n="Bororo" lng="-57.0" lat="-16.0"/>
<l c="cac" n="Cacua" lng="-70.0" lat="1.08333333333"/>
<l c="cnl" n="Canela" lng="-45.0" lat="-7.0"/>
<l c="che" n="Cherokee" lng="-83.5" lat="35.5"/>
<l c="cve" n="Chuave" lng="145.116666667" lat="-6.11666666667"/>
<l c="cmn" n="Comanche" lng="-101.5" lat="33.5"/>
<l c="cre" n="Cree (Plains)" lng="-110.0" lat="54.0"/>
<l c="cub" n="Cubeo" lng="-70.5" lat="1.33333333333"/>
<l c="dad" n="Dadibi" lng="144.583333333" lat="-6.55"/>
<l c="dag" n="Daga" lng="149.333333333" lat="-10.0"/>
<l c="dni" n="Dani (Lower Grand Valley)" lng="138.833333333" lat="-4.33333333333"/>
<l c="der" n="Dla (Proper)" lng="141.0" lat="-3.58333333333"/>
<l c="dum" n="Dumo" lng="141.3" lat="-2.68333333333"/>
<l c="dyi" n="Dyirbal" lng="145.583333333" lat="-17.8333333333"/>
<l c="efi" n="Efik" lng="8.5" lat="4.91666666667"/>
<l c="eka" n="Ekari" lng="135.5" lat="-3.83333333333"/>
<l c="fas" n="Fasu" lng="143.333333333" lat="-6.58333333333"/>
<l c="fuz" n="Fuzhou" lng="119.5" lat="26.0"/>
<l c="gds" n="Gadsup" lng="146.0" lat="-6.25"/>
<l c="goa" n="Goajiro" lng="-72.0" lat="12.0"/>
<l c="ham" n="Hamtai" lng="146.25" lat="-7.5"/>
<l c="haw" n="Hawaiian" lng="-155.5" lat="19.5833333333"/>
<l c="imo" n="Imonda" lng="141.166666667" lat="-3.33333333333"/>
<l c="irr" n="Irarutu" lng="133.5" lat="-3.0"/>
<l c="iwm" n="Iwam" lng="142.0" lat="-4.33333333333"/>
<l c="jpr" n="Japreria" lng="-73.0" lat="10.5"/>
<l c="jom" n="Jomang" lng="30.5" lat="10.5833333333"/>
<l c="kng" n="Kaingang" lng="-52.0" lat="-26.0"/>
<l c="krb" n="Kiribati" lng="173.0" lat="1.33333333333"/>
<l c="kiw" n="Kiwai (Southern)" lng="143.5" lat="-8.0"/>
<l c="kla" n="Klao" lng="-8.75" lat="4.75"/>
<l c="koa" n="Koasati" lng="-85.1666666667" lat="34.8333333333"/>
<l c="koi" n="Koiari" lng="147.333333333" lat="-9.5"/>
<l c="kya" n="Kuku-Yalanji" lng="145.0" lat="-16.0"/>
<l c="mya" n="Ma&#39;ya" lng="130.916666667" lat="-1.25"/>
<l c="mlk" n="Malakmalak" lng="130.416666667" lat="-13.4166666667"/>
<l c="mao" n="Maori" lng="176.0" lat="-40.0"/>
<l c="mrn" n="Maranao" lng="124.25" lat="7.83333333333"/>
<l c="mku" n="Maranungku" lng="130.0" lat="-13.6666666667"/>
<l c="max" n="Maxakalí" lng="-40.0" lat="-18.0"/>
<l c="may" n="Maybrat" lng="132.5" lat="-1.33333333333"/>
<l c="mtp" n="Mixe (Totontepec)" lng="-96.0" lat="17.25"/>
<l c="mor" n="Mor" lng="135.75" lat="-2.95"/>
<l c="nan" n="Nandi" lng="35.0" lat="0.25"/>
<l c="nas" n="Nasioi" lng="155.583333333" lat="-6.33333333333"/>
<l c="nim" n="Nimboran" lng="140.166666667" lat="-2.5"/>
<l c="ond" n="Oneida" lng="-75.6666666667" lat="43.0"/>
<l c="pnr" n="Panare" lng="-66.0" lat="6.5"/>
<l c="paw" n="Pawaian" lng="145.083333333" lat="-7.0"/>
<l c="prh" n="Pirahã" lng="-62.0" lat="-7.0"/>
<l c="poh" n="Pohnpeian" lng="158.25" lat="6.88333333333"/>
<l c="bng" n="Qaqet" lng="152.0" lat="-4.58333333333"/>
<l c="rap" n="Rapanui" lng="-109.366666667" lat="-27.1166666667"/>
<l c="ror" n="Roro" lng="146.583333333" lat="-8.75"/>
<l c="rtk" n="Rotokas" lng="155.166666667" lat="-6.0"/>
<l c="snm" n="Sanuma" lng="-64.6666666667" lat="4.5"/>
<l c="seb" n="Sebei" lng="34.5833333333" lat="1.33333333333"/>
<l c="snc" n="Seneca" lng="-77.5" lat="42.5"/>
<l c="snt" n="Sentani" lng="140.583333333" lat="-2.58333333333"/>
<l c="shi" n="Shiriana" lng="-62.8333333333" lat="3.5"/>
<l c="sue" n="Suena" lng="147.55" lat="-7.75"/>
<l c="ttn" n="Tetun" lng="126.0" lat="-9.0"/>
<l c="tgk" n="Tigak" lng="150.8" lat="-2.71666666667"/>
<l c="toa" n="Toaripi" lng="146.25" lat="-8.33333333333"/>
<l c="usa" n="Usan" lng="145.166666667" lat="-4.83333333333"/>
<l c="bno" n="Waimaha" lng="-70.25" lat="0.333333333333"/>
<l c="wra" n="Warao" lng="-61.6666666667" lat="9.33333333333"/>
<l c="wrs" n="Waris" lng="141.0" lat="-3.16666666667"/>
<l c="wmu" n="Wik Munkan" lng="141.75" lat="-13.9166666667"/>
<l c="ygr" n="Yagaria" lng="145.416666667" lat="-6.33333333333"/>
<l c="yag" n="Yagua" lng="-72.0" lat="-3.5"/>
<l c="yar" n="Yareba" lng="148.5" lat="-9.5"/>
<l c="yaw" n="Yawa" lng="136.25" lat="-1.75"/>
<l c="yid" n="Yidiny" lng="145.75" lat="-17.0"/>
<l c="yim" n="Yimas" lng="143.55" lat="-4.66666666667"/>
</v>
<v numeric="2" description="Moderately small" icon_id="c9999ff" icon_url="https://wals.info/clld-static/icons/c9999ff.png" zindex="0">
<l c="abi" n="Abipón" lng="-61.0" lat="-29.0"/>
<l c="acm" n="Achumawi" lng="-121.0" lat="41.5"/>
<l c="adz" n="Adzera" lng="146.25" lat="-6.25"/>
<l c="ala" n="Alamblak" lng="143.333333333" lat="-4.66666666667"/>
<l c="ame" n="Amele" lng="145.583333333" lat="-5.25"/>
<l c="arp" n="Arapesh (Mountain)" lng="143.166666667" lat="-3.46666666667"/>
<l c="bai" n="Bai" lng="100.0" lat="26.0"/>
<l c="bki" n="Bakairí" lng="-55.0" lat="-14.0"/>
<l c="brd" n="Bardi" lng="122.916666667" lat="-16.5833333333"/>
<l c="brb" n="Bariba" lng="2.5" lat="10.0"/>
<l c="bkr" n="Batak (Karo)" lng="98.25" lat="3.25"/>
<l c="bto" n="Batak (Toba)" lng="99.0" lat="2.5"/>
<l c="bee" n="Beembe" lng="14.0833333333" lat="-3.91666666667"/>
<l c="bis" n="Bisa" lng="-0.5" lat="11.5"/>
<l c="bod" n="Bodo" lng="92.0" lat="26.8333333333"/>
<l c="bri" n="Bribri" lng="-83.0" lat="9.41666666667"/>
<l c="bua" n="Burarra" lng="134.583333333" lat="-12.25"/>
<l c="cax" n="Campa (Axininca)" lng="-74.0" lat="-12.0"/>
<l c="car" n="Carib" lng="-56.0" lat="5.5"/>
<l c="cyv" n="Cayuvava" lng="-65.5" lat="-13.5"/>
<l c="cso" n="Chatino (Sierra Occidental)" lng="-97.3333333333" lat="16.25"/>
<l c="cck" n="Chickasaw" lng="-88.0" lat="34.0"/>
<l c="chk" n="Chukchi" lng="-173.0" lat="67.0"/>
<l c="epe" n="Epena Pedee" lng="-77.0" lat="3.0"/>
<l c="evn" n="Even" lng="130.0" lat="68.0"/>
<l c="eve" n="Evenki" lng="125.0" lat="56.0"/>
<l c="fef" n="Fe&#39;fe&#39;" lng="10.1666666667" lat="5.25"/>
<l c="fin" n="Finnish" lng="25.0" lat="62.0"/>
<l c="fur" n="Fur" lng="25.0" lat="13.5"/>
<l c="gar" n="Garo" lng="90.5" lat="25.6666666667"/>
<l c="ghb" n="Guahibo" lng="-69.0" lat="5.0"/>
<l c="gmb" n="Guambiano" lng="-76.6666666667" lat="2.5"/>
<l c="gua" n="Guaraní" lng="-56.0" lat="-26.0"/>
<l c="hak" n="Hakka" lng="116.0" lat="25.0"/>
<l c="hba" n="Hebrew (Modern Ashkenazic)" lng="35.1666666667" lat="31.75"/>
<l c="hix" n="Hixkaryana" lng="-59.0" lat="-1.0"/>
<l c="hum" n="Huitoto (Murui)" lng="-73.5" lat="-1.0"/>
<l c="ika" n="Ika" lng="-73.75" lat="10.6666666667"/>
<l c="jpn" n="Japanese" lng="140.0" lat="37.0"/>
<l c="jiv" n="Jivaro" lng="-78.0" lat="-2.5"/>
<l c="kly" n="Kala Lagaw Ya" lng="142.116666667" lat="-10.1166666667"/>
<l c="krk" n="Karok" lng="-123.0" lat="41.6666666667"/>
<l c="kay" n="Kayardild" lng="139.5" lat="-17.05"/>
<l c="ked" n="Kedang" lng="123.75" lat="-8.25"/>
<l c="ket" n="Ket" lng="87.0" lat="64.0"/>
<l c="kew" n="Kewa" lng="143.833333333" lat="-6.5"/>
<l c="kty" n="Khanty" lng="65.0" lat="65.0"/>
<l c="kss" n="Kisi (Southern)" lng="-10.25" lat="8.5"/>
<l c="kfe" n="Koromfe" lng="-0.916666666667" lat="14.25"/>
<l c="kry" n="Koryak" lng="167.0" lat="61.0"/>
<l c="kch" n="Koyra Chiini" lng="-3.0" lat="17.0"/>
<l c="kse" n="Koyraboro Senni" lng="0.0" lat="16.0"/>
<l c="kun" n="Kuna" lng="-77.3333333333" lat="8.0"/>
<l c="kmp" n="Kunimaipa" lng="146.833333333" lat="-8.0"/>
<l c="kwa" n="Kwaio" lng="161.0" lat="-8.95"/>
<l c="lan" n="Lango" lng="33.0" lat="2.16666666667"/>
<l c="lav" n="Lavukaleve" lng="159.2" lat="-9.08333333333"/>
<l c="len" n="Lenakel" lng="169.25" lat="-19.45"/>
<l c="kkv" n="Lusi" lng="149.666666667" lat="-5.58333333333"/>
<l c="luv" n="Luvale" lng="22.0" lat="-12.0"/>
<l c="mne" n="Maidu (Northeast)" lng="-120.666666667" lat="40.0"/>
<l c="mnc" n="Manchu" lng="127.5" lat="49.5"/>
<l c="myi" n="Mangarrayi" lng="133.5" lat="-14.6666666667"/>
<l c="mrd" n="Marind" lng="140.166666667" lat="-7.83333333333"/>
<l c="mau" n="Maung" lng="133.5" lat="-11.9166666667"/>
<l c="mss" n="Miwok (Southern Sierra)" lng="-120.0" lat="37.5"/>
<l c="mxc" n="Mixtec (Chalcatongo)" lng="-97.5833333333" lat="17.05"/>
<l c="mxm" n="Mixtec (Molinos)" lng="-97.5833333333" lat="17.0"/>
<l c="mov" n="Movima" lng="-65.6666666667" lat="-13.8333333333"/>
<l c="nhn" n="Nahuatl (North Puebla)" lng="-98.25" lat="20.0"/>
<l c="nht" n="Nahuatl (Tetelcingo)" lng="-99.0" lat="19.6666666667"/>
<l c="nai" n="Nanai" lng="137.0" lat="49.5"/>
<l c="nnc" n="Nancowry" lng="93.5" lat="8.05"/>
<l c="ndy" n="Ndyuka" lng="-54.5" lat="4.5"/>
<l c="nob" n="Nobiin" lng="31.0" lat="21.0"/>
<l c="nyg" n="Nyangi" lng="33.5833333333" lat="3.41666666667"/>
<l c="nyi" n="Nyimang" lng="29.3333333333" lat="12.1666666667"/>
<l c="nis" n="Nyishi" lng="93.5" lat="27.5"/>
<l c="oji" n="Ojibwa (Eastern)" lng="-80.0" lat="46.0"/>
<l c="pms" n="Paamese" lng="168.25" lat="-16.5"/>
<l c="psm" n="Passamaquoddy-Maliseet" lng="-67.0" lat="45.0"/>
<l c="pec" n="Pech" lng="-85.5" lat="15.0"/>
<l c="pit" n="Pitjantjatjara" lng="130.0" lat="-26.0"/>
<l c="poa" n="Po-Ai" lng="164.833333333" lat="-20.6666666667"/>
<l c="ram" n="Rama" lng="-83.75" lat="11.75"/>
<l c="svs" n="Savosavo" lng="159.8" lat="-9.13333333333"/>
<l c="slp" n="Selepet" lng="147.166666667" lat="-6.16666666667"/>
<l c="skp" n="Selkup" lng="82.0" lat="65.0"/>
<l c="shs" n="Shasta" lng="-122.666666667" lat="41.8333333333"/>
<l c="shk" n="Shipibo-Konibo" lng="-75.0" lat="-7.5"/>
<l c="sin" n="Siona" lng="-76.25" lat="0.333333333333"/>
<l c="sor" n="Sora" lng="84.3333333333" lat="20.0"/>
<l c="tab" n="Taba" lng="127.5" lat="0.0"/>
<l c="tac" n="Tacana" lng="-68.0" lat="-13.5"/>
<l c="tag" n="Tagalog" lng="121.0" lat="15.0"/>
<l c="tsg" n="Tausug" lng="121.0" lat="6.0"/>
<l c="tmn" n="Temein" lng="29.4166666667" lat="11.9166666667"/>
<l c="tne" n="Temne" lng="-13.0833333333" lat="8.66666666667"/>
<l c="tic" n="Ticuna" lng="-70.5" lat="-4.0"/>
<l c="try" n="Tiruray" lng="124.166666667" lat="6.75"/>
<l c="ton" n="Tonkawa" lng="-96.75" lat="30.25"/>
<l c="dts" n="Toro So" lng="-3.25" lat="14.4166666667"/>
<l c="tpa" n="Totonac (Papantla)" lng="-97.3333333333" lat="20.3333333333"/>
<l c="tso" n="Tsou" lng="120.75" lat="23.5"/>
<l c="tun" n="Tunica" lng="-91.0" lat="32.6666666667"/>
<l c="ung" n="Ungarinjin" lng="126.0" lat="-16.3333333333"/>
<l c="urk" n="Urubú-Kaapor" lng="-46.5" lat="-2.33333333333"/>
<l c="wah" n="Wahgi" lng="144.716666667" lat="-5.83333333333"/>
<l c="wam" n="Wambaya" lng="135.75" lat="-18.6666666667"/>
<l c="wnt" n="Wantoat" lng="146.5" lat="-6.16666666667"/>
<l c="wps" n="Wapishana" lng="-60.0" lat="2.66666666667"/>
<l c="wry" n="Waray (in Australia)" lng="131.25" lat="-13.1666666667"/>
<l c="wrd" n="Wardaman" lng="131.0" lat="-15.5"/>
<l c="war" n="Wari&#39;" lng="-65.0" lat="-11.3333333333"/>
<l c="wma" n="West Makian" lng="127.583333333" lat="0.5"/>
<l c="wdo" n="Western Desert (Ooldea)" lng="132.0" lat="-30.5"/>
<l c="woi" n="Woisika" lng="124.833333333" lat="-8.25"/>
<l c="yaq" n="Yaqui" lng="-110.25" lat="27.5"/>
<l c="yes" n="Yessan-Mayo" lng="142.583333333" lat="-4.16666666667"/>
<l c="yor" n="Yoruba" lng="4.33333333333" lat="8.0"/>
<l c="ycn" n="Yucuna" lng="-71.0" lat="-0.75"/>
<l c="zqc" n="Zoque (Copainalá)" lng="-93.25" lat="17.0"/>
</v>
<v numeric="3" description="Average" icon_id="cffffff" icon_url="https://wals.info/clld-static/icons/cffffff.png" zindex="0">
<l c="agh" n="Aghem" lng="10.0" lat="6.66666666667"/>
<l c="aik" n="Aikaná" lng="-60.6666666667" lat="-12.6666666667"/>
<l c="aiz" n="Aizi" lng="-4.5" lat="5.25"/>
<l c="akn" n="Akan" lng="-1.25" lat="6.5"/>
<l c="alw" n="Alawa" lng="134.25" lat="-15.1666666667"/>
<l c="alb" n="Albanian" lng="20.0" lat="41.0"/>
<l c="aea" n="Aleut (Eastern)" lng="-164.0" lat="54.75"/>
<l c="ald" n="Alladian" lng="-4.33333333333" lat="5.16666666667"/>
<l c="amo" n="Amo" lng="8.66666666667" lat="10.3333333333"/>
<l c="amu" n="Amuesha" lng="-75.4166666667" lat="-10.5"/>
<l c="amz" n="Amuzgo" lng="-98.0" lat="16.8333333333"/>
<l c="ana" n="Araona" lng="-67.75" lat="-12.3333333333"/>
<l c="ata" n="Atayal" lng="121.333333333" lat="24.5"/>
<l c="aze" n="Azerbaijani" lng="48.5" lat="40.5"/>
<l c="bam" n="Bambara" lng="-7.5" lat="12.5"/>
<l c="bsq" n="Basque" lng="-3.0" lat="43.0"/>
<l c="baw" n="Bawm" lng="92.25" lat="22.5"/>
<l c="bej" n="Beja" lng="36.0" lat="18.0"/>
<l c="ber" n="Berta" lng="34.6666666667" lat="10.3333333333"/>
<l c="bir" n="Birom" lng="8.83333333333" lat="9.66666666667"/>
<l c="bbf" n="Bobo Madaré (Northern)" lng="-4.3333333333333" lat="12.4166666666667"/>
<l c="brh" n="Brahui" lng="67.0" lat="28.5"/>
<l c="bra" n="Brao" lng="107.5" lat="14.1666666667"/>
<l c="bre" n="Breton" lng="-3.0" lat="48.0"/>
<l c="brw" n="Bru (Western)" lng="104.75" lat="16.75"/>
<l c="bul" n="Bulgarian" lng="25.0" lat="42.5"/>
<l c="bet" n="Bété" lng="-6.25" lat="6.25"/>
<l c="cad" n="Caddo" lng="-93.5" lat="33.3333333333"/>
<l c="cah" n="Cahuilla" lng="-116.25" lat="33.5"/>
<l c="cam" n="Camsá" lng="-77.0" lat="1.16666666667"/>
<l c="cnt" n="Cantonese" lng="113.0" lat="23.0"/>
<l c="ctl" n="Catalan" lng="2.0" lat="41.75"/>
<l c="cay" n="Cayapa" lng="-79.0" lat="0.666666666667"/>
<l c="chw" n="Cham (Western)" lng="105.5" lat="12.0"/>
<l c="cha" n="Chamorro" lng="144.75" lat="13.45"/>
<l c="cti" n="Chin (Tiddim)" lng="93.6666666667" lat="23.3333333333"/>
<l c="cle" n="Chinantec (Lealao)" lng="-95.9166666667" lat="17.3333333333"/>
<l c="chv" n="Chuvash" lng="47.5" lat="55.5"/>
<l c="cil" n="CiLuba" lng="22.0" lat="-6.0"/>
<l c="ccp" n="Cocopa" lng="-115.0" lat="32.3333333333"/>
<l c="dgb" n="Dagbani" lng="-0.5" lat="9.58333333333"/>
<l c="dgr" n="Dagur" lng="124.0" lat="48.0"/>
<l c="ddf" n="Daju (Dar Fur)" lng="25.25" lat="12.25"/>
<l c="dan" n="Dan" lng="-8.0" lat="7.5"/>
<l c="dnw" n="Dangaléat (Western)" lng="18.3333333333" lat="12.1666666667"/>
<l c="die" n="Diegueño (Mesa Grande)" lng="-116.166666667" lat="32.6666666667"/>
<l c="din" n="Dinka" lng="28.0" lat="8.5"/>
<l c="dio" n="Diola-Fogny" lng="-16.25" lat="13.0"/>
<l c="diy" n="Diyari" lng="139.0" lat="-28.0"/>
<l c="diz" n="Dizi" lng="36.5" lat="6.16666666667"/>
<l c="djp" n="Djapu" lng="136.0" lat="-12.6666666667"/>
<l c="don" n="Dong (Southern)" lng="109.0" lat="27.0"/>
<l c="doy" n="Doyayo" lng="13.0833333333" lat="8.66666666667"/>
<l c="eja" n="Ejagham" lng="8.66666666667" lat="5.41666666667"/>
<l c="eng" n="English" lng="0.0" lat="52.0"/>
<l c="fij" n="Fijian" lng="178.0" lat="-17.8333333333"/>
<l c="fre" n="French" lng="2.0" lat="48.0"/>
<l c="ful" n="Fulniô" lng="-37.5" lat="-8.0"/>
<l c="grr" n="Garrwa" lng="137.166666667" lat="-17.0833333333"/>
<l c="ger" n="German" lng="10.0" lat="52.0"/>
<l c="goo" n="Gooniyandi" lng="126.333333333" lat="-18.3333333333"/>
<l c="gan" n="Great Andamanese" lng="92.6666666667" lat="12.0"/>
<l c="grb" n="Grebo" lng="-8.0" lat="5.0"/>
<l c="grk" n="Greek (Modern)" lng="22.0" lat="39.0"/>
<l c="grw" n="Greenlandic (West)" lng="-51.0" lat="64.0"/>
<l c="gwa" n="Gwari" lng="7.0" lat="9.5"/>
<l c="hmr" n="Hamer" lng="36.5" lat="5.0"/>
<l c="hop" n="Hopi" lng="-110.0" lat="36.0"/>
<l c="htc" n="Huastec" lng="-99.3333333333" lat="22.0833333333"/>
<l c="hve" n="Huave (San Mateo del Mar)" lng="-95.0" lat="16.2166666667"/>
<l c="iba" n="Iban" lng="112.0" lat="2.0"/>
<l c="ign" n="Ignaciano" lng="-65.4166666667" lat="-15.1666666667"/>
<l c="ijo" n="Ijo (Kolokuma)" lng="5.66666666667" lat="4.91666666667"/>
<l c="ind" n="Indonesian" lng="106.0" lat="0.0"/>
<l c="igs" n="Ingessana" lng="34.0" lat="11.5"/>
<l c="irx" n="Iranxe" lng="-58.0" lat="-13.0"/>
<l c="ito" n="Itonama" lng="-64.3333333333" lat="-12.8333333333"/>
<l c="iva" n="Ivatan" lng="122.0" lat="20.5"/>
<l c="jav" n="Javanese" lng="111.0" lat="-7.0"/>
<l c="jeb" n="Jebero" lng="-76.5" lat="-5.41666666667"/>
<l c="jng" n="Jingpho" lng="97.0" lat="25.4166666667"/>
<l c="kek" n="K&#39;ekchí" lng="-89.8333333333" lat="16.0"/>
<l c="kad" n="Kadugli" lng="29.6666666667" lat="11.0"/>
<l c="kgu" n="Kalkatungu" lng="139.5" lat="-21.0"/>
<l c="knk" n="Kanakuru" lng="12.0" lat="10.0"/>
<l c="knr" n="Kanuri" lng="13.0" lat="12.0"/>
<l c="kws" n="Kawaiisu" lng="-117.5" lat="36.0"/>
<l c="kyl" n="Kayah Li (Eastern)" lng="97.5" lat="19.0"/>
<l c="kef" n="Kefa" lng="36.25" lat="7.25"/>
<l c="ker" n="Kera" lng="15.0833333333" lat="9.83333333333"/>
<l c="kha" n="Khalkha" lng="105.0" lat="47.0"/>
<l c="khs" n="Khasi" lng="92.0" lat="25.5"/>
<l c="khm" n="Khmer" lng="105.0" lat="12.5"/>
<l c="kmu" n="Khmu&#39;" lng="102.0" lat="21.0"/>
<l c="klv" n="Kilivila" lng="151.083333333" lat="-8.5"/>
<l c="kio" n="Kiowa" lng="-99.0" lat="37.0"/>
<l c="kgz" n="Kirghiz" lng="75.0" lat="42.0"/>
<l c="kob" n="Kobon" lng="144.333333333" lat="-5.16666666667"/>
<l c="kom" n="Komo" lng="33.75" lat="8.75"/>
<l c="kkn" n="Konkani" lng="74.0" lat="15.25"/>
<l c="kor" n="Korean" lng="128.0" lat="37.5"/>
<l c="kot" n="Kota" lng="77.1666666667" lat="11.5"/>
<l c="koy" n="Koya" lng="81.3333333333" lat="17.5"/>
<l c="kpa" n="Kpan" lng="10.1666666667" lat="7.58333333333"/>
<l c="kpe" n="Kpelle" lng="-10.0" lat="7.0"/>
<l c="kro" n="Krongo" lng="30.0" lat="10.5"/>
<l c="kul" n="Kullo" lng="37.0833333333" lat="6.75"/>
<l c="knm" n="Kunama" lng="37.0" lat="14.5"/>
<l c="kur" n="Kurukh" lng="85.5" lat="22.8333333333"/>
<l c="kwo" n="Kwoma" lng="142.75" lat="-4.16666666667"/>
<l c="lkt" n="Lakhota" lng="-101.833333333" lat="43.8333333333"/>
<l c="llm" n="Lelemi" lng="0.5" lat="7.33333333333"/>
<l c="lua" n="Lua" lng="17.75" lat="9.75"/>
<l c="lui" n="Luiseño" lng="-117.166666667" lat="33.3333333333"/>
<l c="lu" n="Lü" lng="100.666666667" lat="22.0"/>
<l c="maa" n="Maasai" lng="36.0" lat="-3.0"/>
<l c="mab" n="Maba" lng="20.8333333333" lat="13.75"/>
<l c="mla" n="Mambila" lng="11.5" lat="6.75"/>
<l c="mnd" n="Mandarin" lng="110.0" lat="34.0"/>
<l c="mgg" n="Mangghuer" lng="102.0" lat="36.0"/>
<l c="map" n="Mapudungun" lng="-72.0" lat="-38.0"/>
<l c="mme" n="Mari (Meadow)" lng="48.0" lat="57.0"/>
<l c="mar" n="Maricopa" lng="-113.166666667" lat="33.1666666667"/>
<l c="mrt" n="Martuthunira" lng="116.5" lat="-20.8333333333"/>
<l c="mzc" n="Mazatec (Chiquihuitlán)" lng="-96.9166666667" lat="17.75"/>
<l c="mba" n="Mba" lng="25.0" lat="1.0"/>
<l c="mbb" n="Mbabaram" lng="145.0" lat="-17.1666666667"/>
<l c="mei" n="Meithei" lng="94.0" lat="24.75"/>
<l c="hok" n="Min (Southern)" lng="118.0" lat="25.0"/>
<l c="mog" n="Moghol" lng="62.0" lat="35.0"/>
<l c="mro" n="Moro" lng="30.1666666667" lat="11.0"/>
<l c="mui" n="Muinane" lng="-72.5" lat="-1.0"/>
<l c="mum" n="Mumuye" lng="11.6666666667" lat="9.0"/>
<l c="mrl" n="Murle" lng="33.5" lat="6.5"/>
<l c="mpa" n="Murrinh-Patha" lng="129.666666667" lat="-14.6666666667"/>
<l c="nmb" n="Nambikuára (Southern)" lng="-59.5" lat="-14.0"/>
<l c="nar" n="Nara (in Ethiopia)" lng="37.5833333333" lat="15.0833333333"/>
<l c="nap" n="Neo-Aramaic (Persian Azerbaijan)" lng="47.0" lat="38.0"/>
<l c="new" n="Newari (Kathmandu)" lng="85.5" lat="27.6666666667"/>
<l c="nga" n="Nganasan" lng="93.0" lat="71.0"/>
<l c="chu" n="Nivacle" lng="-60.5" lat="-23.5"/>
<l c="nko" n="Nkore-Kiga" lng="29.8333333333" lat="-0.916666666667"/>
<l c="non" n="Noni" lng="10.5833333333" lat="6.41666666667"/>
<l c="nor" n="Norwegian" lng="8.0" lat="61.0"/>
<l c="nun" n="Nung (in Vietnam)" lng="106.416666667" lat="21.9166666667"/>
<l c="nug" n="Nunggubuyu" lng="135.666666667" lat="-13.75"/>
<l c="ood" n="O&#39;odham" lng="-112.0" lat="32.0"/>
<l c="ogb" n="Ogbia" lng="6.25" lat="4.66666666667"/>
<l c="orm" n="Ormuri" lng="69.75" lat="32.5"/>
<l c="otm" n="Otomí (Mezquital)" lng="-99.1666666667" lat="20.1666666667"/>
<l c="pac" n="Pacoh" lng="107.083333333" lat="16.4166666667"/>
<l c="pai" n="Paiwan" lng="120.833333333" lat="22.5"/>
<l c="pau" n="Paumarí" lng="-64.0" lat="-6.0"/>
<l c="prs" n="Persian" lng="54.0" lat="32.0"/>
<l c="phl" n="Phlong" lng="99.0" lat="15.0"/>
<l c="qaw" n="Qawasqar" lng="-75.0" lat="-49.0"/>
<l c="rom" n="Romanian" lng="25.0" lat="46.0"/>
<l c="rsc" n="Romansch (Scharans)" lng="9.5" lat="46.75"/>
<l c="ruk" n="Rukai (Tanan)" lng="120.833333333" lat="22.8333333333"/>
<l c="sab" n="Sa&#39;ban" lng="115.666666667" lat="3.66666666667"/>
<l c="sel" n="Selknam" lng="-70.0" lat="-53.0"/>
<l c="snd" n="Senadi" lng="-6.25" lat="9.5"/>
<l c="sha" n="Shan" lng="98.0" lat="22.0"/>
<l c="snh" n="Sinhala" lng="80.5" lat="7.0"/>
<l c="srn" n="Sirionó" lng="-64.0" lat="-15.5833333333"/>
<l c="som" n="Somali" lng="45.0" lat="3.0"/>
<l c="spa" n="Spanish" lng="-4.0" lat="40.0"/>
<l c="sup" n="Supyire" lng="-5.58333333333" lat="11.5"/>
<l c="sba" n="Sáliba (in Colombia)" lng="-70.0" lat="6.0"/>
<l c="tma" n="Tama" lng="22.0" lat="14.5"/>
<l c="tam" n="Tamang (Eastern)" lng="85.666666666667" lat="27.5"/>
<l c="tmp" n="Tampulma" lng="-0.583333333333" lat="10.4166666667"/>
<l c="tks" n="Teke (Southern)" lng="14.5" lat="-2.33333333333"/>
<l c="tha" n="Thai" lng="101.0" lat="16.0"/>
<l c="tiw" n="Tiwi" lng="131.0" lat="-11.5"/>
<l c="tlp" n="Tlapanec" lng="-99.0" lat="17.0833333333"/>
<l c="tol" n="Tol" lng="-87.0" lat="14.6666666667"/>
<l c="tru" n="Trumai" lng="-53.5833333333" lat="-11.9166666667"/>
<l c="tug" n="Tuareg (Ahaggar)" lng="6.0" lat="23.0"/>
<l c="tuk" n="Tukang Besi" lng="123.5" lat="-5.5"/>
<l c="tul" n="Tulu" lng="75.3333333333" lat="12.75"/>
<l c="tur" n="Turkish" lng="35.0" lat="39.0"/>
<l c="tuv" n="Tuvan" lng="95.0" lat="52.0"/>
<l c="tza" n="Tzeltal (Aguacatenango)" lng="-92.5" lat="16.4166666667"/>
<l c="umb" n="UMbundu" lng="15.0" lat="-12.5"/>
<l c="una" n="Una" lng="140.0" lat="-4.66666666667"/>
<l c="uzn" n="Uzbek (Northern)" lng="66.5" lat="40.6666666667"/>
<l c="vie" n="Vietnamese" lng="106.5" lat="10.5"/>
<l c="wic" n="Wichita" lng="-97.3333333333" lat="33.3333333333"/>
<l c="wch" n="Wichí" lng="-62.5833333333" lat="-22.5"/>
<l c="wiy" n="Wiyot" lng="-124.166666667" lat="40.8333333333"/>
<l c="wuc" n="Wu" lng="119.916666667" lat="31.6666666667"/>
<l c="ykt" n="Yakut" lng="130.0" lat="62.0"/>
<l c="yan" n="Yana" lng="-122.0" lat="40.5"/>
<l c="yap" n="Yapese" lng="138.166666667" lat="9.58333333333"/>
<l c="yay" n="Yay" lng="104.75" lat="22.4166666667"/>
<l c="yct" n="Yucatec" lng="-89.0" lat="20.0"/>
<l c="yko" n="Yukaghir (Kolyma)" lng="150.833333333" lat="65.75"/>
<l c="ytu" n="Yukaghir (Tundra)" lng="155.0" lat="69.0"/>
<l c="zan" n="Zande" lng="26.0" lat="4.0"/>
<l c="zun" n="Zuni" lng="-108.833333333" lat="35.0833333333"/>
</v>
<v numeric="4" description="Moderately large" icon_id="cff66ff" icon_url="https://wals.info/clld-static/icons/cff66ff.png" zindex="0">
<l c="aht" n="Ahtna" lng="-145.0" lat="62.0"/>
<l c="amh" n="Amharic" lng="38.0" lat="10.0"/>
<l c="anc" n="Angas" lng="9.5" lat="9.5"/>
<l c="aeg" n="Arabic (Egyptian)" lng="31.0" lat="30.0"/>
<l c="arm" n="Armenian (Eastern)" lng="45.0" lat="40.0"/>
<l c="awn" n="Awngi" lng="36.6666666667" lat="10.8333333333"/>
<l c="aym" n="Aymara (Central)" lng="-69.0" lat="-17.0"/>
<l c="bag" n="Bagirmi" lng="16.0" lat="11.6666666667"/>
<l c="baj" n="Bajau (Sama)" lng="123.0" lat="-4.33333333333"/>
<l c="bsk" n="Bashkir" lng="58.0" lat="53.0"/>
<l c="bco" n="Bella Coola" lng="-126.666666667" lat="52.5"/>
<l c="ben" n="Bengali" lng="90.0" lat="24.0"/>
<l c="bma" n="Berber (Middle Atlas)" lng="-5.0" lat="33.0"/>
<l c="brm" n="Burmese" lng="96.0" lat="21.0"/>
<l c="chl" n="Chehalis (Upper)" lng="-123.0" lat="46.5833333333"/>
<l c="chq" n="Chinantec (Quiotepec)" lng="-96.6666666667" lat="17.5833333333"/>
<l c="cof" n="Cofán" lng="-77.1666666667" lat="0.166666666667"/>
<l c="dar" n="Darai" lng="84.0" lat="24.0"/>
<l c="dre" n="Drehu" lng="167.25" lat="-21.0"/>
<l c="ewe" n="Ewe" lng="0.416666666667" lat="6.33333333333"/>
<l c="ewo" n="Ewondo" lng="12.0" lat="4.0"/>
<l c="eya" n="Eyak" lng="-145.0" lat="60.5"/>
<l c="gbb" n="Gbeya Bossangoa" lng="17.5" lat="6.66666666667"/>
<l c="gla" n="Gelao" lng="105.5" lat="22.9166666667"/>
<l c="geo" n="Georgian" lng="44.0" lat="42.0"/>
<l c="ga" n="Gã" lng="-0.166666666667" lat="5.66666666667"/>
<l c="hau" n="Hausa" lng="7.0" lat="12.0"/>
<l c="hun" n="Hungarian" lng="20.0" lat="47.0"/>
<l c="hup" n="Hupa" lng="-123.666666667" lat="41.0833333333"/>
<l c="igb" n="Igbo" lng="7.33333333333" lat="6.0"/>
<l c="ik" n="Ik" lng="34.1666666667" lat="3.75"/>
<l c="irq" n="Iraqw" lng="35.5" lat="-4.0"/>
<l c="iso" n="Isoko" lng="6.25" lat="5.5"/>
<l c="ite" n="Itelmen" lng="157.5" lat="57.0"/>
<l c="jak" n="Jakaltek" lng="-91.6666666667" lat="15.6666666667"/>
<l c="knd" n="Kannada" lng="76.0" lat="14.0"/>
<l c="ksg" n="Karen (Sgaw)" lng="97.0" lat="18.0"/>
<l c="kas" n="Kashmiri" lng="76.0" lat="34.0"/>
<l c="khr" n="Kharia" lng="84.3333333333" lat="22.5"/>
<l c="klm" n="Klamath" lng="-121.5" lat="42.5"/>
<l c="koh" n="Kohumono" lng="8.11666666667" lat="6.0"/>
<l c="kzy" n="Komi-Zyrian" lng="55.0" lat="65.0"/>
<l c="ktk" n="Kotoko" lng="15.3333333333" lat="11.3333333333"/>
<l c="krd" n="Kurdish (Central)" lng="44.0" lat="36.0"/>
<l c="kut" n="Kutenai" lng="-116.0" lat="49.5"/>
<l c="lad" n="Ladakhi" lng="78.0" lat="34.0"/>
<l c="lah" n="Lahu" lng="98.1666666667" lat="20.0"/>
<l c="lkk" n="Lakkia" lng="110.166666667" lat="24.0833333333"/>
<l c="lam" n="Lamé" lng="14.5" lat="9.0"/>
<l c="lat" n="Latvian" lng="24.0" lat="57.0"/>
<l c="lep" n="Lepcha" lng="88.5" lat="27.1666666667"/>
<l c="lug" n="Lugbara" lng="30.9166666667" lat="3.08333333333"/>
<l c="luo" n="Luo" lng="34.75" lat="-0.5"/>
<l c="mal" n="Malagasy" lng="47.0" lat="-20.0"/>
<l c="mrg" n="Margi" lng="13.0" lat="11.0"/>
<l c="mbm" n="Mbum" lng="13.1666666667" lat="7.75"/>
<l c="mie" n="Mien" lng="111.0" lat="25.0"/>
<l c="mun" n="Mundari" lng="84.6666666667" lat="23.0"/>
<l c="kho" n="Nama" lng="18.0" lat="-25.5"/>
<l c="nbk" n="Natügu" lng="165.866666667" lat="-10.7833333333"/>
<l c="nav" n="Navajo" lng="-108.0" lat="36.1666666667"/>
<l c="ndt" n="Ndut" lng="-16.9166666667" lat="14.9166666667"/>
<l c="ntu" n="Nenets" lng="76.0" lat="70.0"/>
<l c="nep" n="Nepali" lng="85.0" lat="28.0"/>
<l c="nez" n="Nez Perce" lng="-116.0" lat="46.0"/>
<l c="niv" n="Nivkh" lng="142.0" lat="53.3333333333"/>
<l c="nkt" n="Nyah Kur (Tha Pong)" lng="101.666666667" lat="15.6666666667"/>
<l c="oca" n="Ocaina" lng="-71.75" lat="-2.75"/>
<l c="orh" n="Oromo (Harar)" lng="42.0" lat="9.0"/>
<l c="psh" n="Pashto" lng="67.0" lat="33.0"/>
<l c="pso" n="Pomo (Southeastern)" lng="-122.5" lat="39.0"/>
<l c="pur" n="Purépecha" lng="-101.666666667" lat="19.5"/>
<l c="qco" n="Quechua (Cochabamba)" lng="-66.0" lat="-17.5"/>
<l c="qui" n="Quileute" lng="-124.25" lat="47.9166666667"/>
<l c="res" n="Resígaro" lng="-71.5" lat="-2.41666666667"/>
<l c="rus" n="Russian" lng="38.0" lat="56.0"/>
<l c="san" n="Sango" lng="18.0" lat="5.0"/>
<l c="sml" n="Semelai" lng="103.0" lat="3.0"/>
<l c="sla" n="Slave" lng="-125.0" lat="67.0"/>
<l c="soq" n="Soqotri" lng="54.0" lat="12.5"/>
<l c="sre" n="Sre" lng="108.0" lat="11.5"/>
<l c="swa" n="Swahili" lng="39.0" lat="-6.5"/>
<l c="tok" n="Tarok" lng="10.0833333333" lat="9.0"/>
<l c="teh" n="Tehuelche" lng="-68.0" lat="-48.0"/>
<l c="tel" n="Telugu" lng="79.0" lat="16.0"/>
<l c="tgr" n="Tigré" lng="38.5" lat="16.5"/>
<l c="twn" n="Tiwa (Northern)" lng="-105.5" lat="36.5"/>
<l c="wap" n="Wappo" lng="-122.5" lat="38.5"/>
<l c="win" n="Wintu" lng="-122.5" lat="41.0"/>
<l c="wlf" n="Wolof" lng="-16.0" lat="15.25"/>
<l c="yny" n="Yanyuwa" lng="137.166666667" lat="-16.4166666667"/>
<l c="yus" n="Yupik (Siberian)" lng="-173.0" lat="65.0"/>
<l c="yur" n="Yurok" lng="-124.0" lat="41.3333333333"/>
<l c="zul" n="Zulu" lng="30.0" lat="-30.0"/>
</v>
<v numeric="5" description="Large" icon_id="cdd0000" icon_url="https://wals.info/clld-static/icons/cdd0000.png" zindex="0">
<l c="xoo" n="!Xóõ" lng="21.5" lat="-24.0"/>
<l c="ani" n="//Ani" lng="21.9166666667" lat="-18.9166666667"/>
<l c="abk" n="Abkhaz" lng="41.0" lat="43.0833333333"/>
<l c="aco" n="Acoma" lng="-107.583333333" lat="34.9166666667"/>
<l c="arc" n="Archi" lng="46.8333333333" lat="42.0"/>
<l c="amp" n="Arrernte (Mparntwe)" lng="136.0" lat="-24.0"/>
<l c="ava" n="Avar" lng="46.5" lat="42.5"/>
<l c="bur" n="Burushaski" lng="74.5" lat="36.5"/>
<l c="chp" n="Chipewyan" lng="-106.0" lat="59.0"/>
<l c="coo" n="Coos (Hanis)" lng="-124.166666667" lat="43.5"/>
<l c="dah" n="Dahalo" lng="40.5" lat="-2.33333333333"/>
<l c="det" n="Deti" lng="24.5" lat="-20.5"/>
<l c="fye" n="Fyem" lng="9.33333333333" lat="9.58333333333"/>
<l c="had" n="Hadza" lng="35.1666666667" lat="-3.75"/>
<l c="hai" n="Haida" lng="-132.0" lat="53.0"/>
<l c="hin" n="Hindi" lng="77.0" lat="25.0"/>
<l c="hmo" n="Hmong Njua" lng="105.0" lat="28.0"/>
<l c="hzb" n="Hunzib" lng="46.25" lat="42.1666666667"/>
<l c="iaa" n="Iaai" lng="166.583333333" lat="-20.4166666667"/>
<l c="ing" n="Ingush" lng="45.0833333333" lat="43.1666666667"/>
<l c="ird" n="Irish (Donegal)" lng="-8.0" lat="55.0"/>
<l c="jaq" n="Jaqaru" lng="-76.0" lat="-13.0"/>
<l c="jeh" n="Jeh" lng="107.833333333" lat="15.1666666667"/>
<l c="juh" n="Ju|&#39;hoan" lng="21.0" lat="-19.0"/>
<l c="kab" n="Kabardian" lng="43.5" lat="43.5"/>
<l c="kal" n="Kalami" lng="72.5" lat="35.5"/>
<l c="kgi" n="Konyagi" lng="-13.25" lat="12.5"/>
<l c="kwk" n="Kwakw&#39;ala" lng="-127.0" lat="51.0"/>
<l c="lak" n="Lak" lng="47.1666666667" lat="42.1666666667"/>
<l c="lez" n="Lezgian" lng="47.8333333333" lat="41.6666666667"/>
<l c="lit" n="Lithuanian" lng="24.0" lat="55.0"/>
<l c="lus" n="Lushootseed" lng="-122.0" lat="48.0"/>
<l c="maz" n="Mazahua" lng="-99.9166666667" lat="19.4166666667"/>
<l c="nax" n="Naxi" lng="100.0" lat="27.5"/>
<l c="nti" n="Ngiti" lng="30.25" lat="1.33333333333"/>
<l c="ngz" n="Ngizim" lng="10.9166666667" lat="12.0833333333"/>
<l c="nuu" n="Nuuchahnulth" lng="-126.666666667" lat="49.6666666667"/>
<l c="puk" n="Parauk" lng="99.5" lat="23.25"/>
<l c="pol" n="Polish" lng="20.0" lat="52.0"/>
<l c="pae" n="Páez" lng="-76.0" lat="2.66666666667"/>
<l c="rut" n="Rutul" lng="47.4166666667" lat="41.5"/>
<l c="scs" n="Saami (Central-South)" lng="16.75" lat="64.6666666667"/>
<l c="sdw" n="Sandawe" lng="35.0" lat="-5.0"/>
<l c="sed" n="Sedang" lng="108.0" lat="14.8333333333"/>
<l c="shu" n="Shuswap" lng="-120.0" lat="52.0"/>
<l c="sdh" n="Sindhi" lng="69.0" lat="26.0"/>
<l c="squ" n="Squamish" lng="-123.166666667" lat="49.6666666667"/>
<l c="sui" n="Sui" lng="107.5" lat="26.0"/>
<l c="ter" n="Tera" lng="11.8333333333" lat="11.0"/>
<l c="tib" n="Tibetan (Standard Spoken)" lng="91.0" lat="30.0"/>
<l c="tli" n="Tlingit" lng="-135.0" lat="59.0"/>
<l c="tsi" n="Tsimshian (Coast)" lng="-129.0" lat="52.5"/>
<l c="ttu" n="Tsova-Tush" lng="45.5" lat="42.5"/>
<l c="yel" n="Yelî Dnye" lng="154.166666667" lat="-11.3666666667"/>
<l c="yey" n="Yeyi" lng="23.5" lat="-20.0"/>
<l c="yuc" n="Yuchi" lng="-86.75" lat="35.75"/>
<l c="yul" n="Yulu" lng="25.25" lat="8.5"/>
</v>
</feature>
"""

WALS_2A_VOWELS = """
<feature number="2A" base_url="https://wals.info/" name="Vowel Quality Inventories">
<description>
<url>https://wals.info/feature/2A.xml</url>
<timestamp>2024-10-18T11:59:12.029308+02:00</timestamp>
</description>
<v numeric="1" description="Small (2-4)" icon_id="c0000dd" icon_url="https://wals.info/clld-static/icons/c0000dd.png" zindex="0">
<l c="abk" n="Abkhaz" lng="41.0" lat="43.0833333333"/>
<l c="adz" n="Adzera" lng="146.25" lat="-6.25"/>
<l c="abm" n="Alabama" lng="-87.4166666667" lat="32.3333333333"/>
<l c="alw" n="Alawa" lng="134.25" lat="-15.1666666667"/>
<l c="aea" n="Aleut (Eastern)" lng="-164.0" lat="54.75"/>
<l c="amc" n="Amahuaca" lng="-72.5" lat="-10.5"/>
<l c="amu" n="Amuesha" lng="-75.4166666667" lat="-10.5"/>
<l c="ana" n="Araona" lng="-67.75" lat="-12.3333333333"/>
<l c="amp" n="Arrernte (Mparntwe)" lng="136.0" lat="-24.0"/>
<l c="awp" n="Awa Pit" lng="-78.25" lat="1.5"/>
<l c="aym" n="Aymara (Central)" lng="-69.0" lat="-17.0"/>
<l c="byu" n="Bandjalang (Yugumbir)" lng="153.0" lat="-27.9166666667"/>
<l c="brd" n="Bardi" lng="122.916666667" lat="-16.5833333333"/>
<l c="bco" n="Bella Coola" lng="-126.666666667" lat="52.5"/>
<l c="bma" n="Berber (Middle Atlas)" lng="-5.0" lat="33.0"/>
<l c="cad" n="Caddo" lng="-93.5" lat="33.3333333333"/>
<l c="cah" n="Cahuilla" lng="-116.25" lat="33.5"/>
<l c="cax" n="Campa (Axininca)" lng="-74.0" lat="-12.0"/>
<l c="cay" n="Cayapa" lng="-79.0" lat="0.666666666667"/>
<l c="chl" n="Chehalis (Upper)" lng="-123.0" lat="46.5833333333"/>
<l c="cck" n="Chickasaw" lng="-88.0" lat="34.0"/>
<l c="ccp" n="Cocopa" lng="-115.0" lat="32.3333333333"/>
<l c="cre" n="Cree (Plains)" lng="-110.0" lat="54.0"/>
<l c="diy" n="Diyari" lng="139.0" lat="-28.0"/>
<l c="djp" n="Djapu" lng="136.0" lat="-12.6666666667"/>
<l c="dyi" n="Dyirbal" lng="145.583333333" lat="-17.8333333333"/>
<l c="eya" n="Eyak" lng="-145.0" lat="60.5"/>
<l c="gds" n="Gadsup" lng="146.0" lat="-6.25"/>
<l c="grr" n="Garrwa" lng="137.166666667" lat="-17.0833333333"/>
<l c="goo" n="Gooniyandi" lng="126.333333333" lat="-18.3333333333"/>
<l c="grw" n="Greenlandic (West)" lng="-51.0" lat="64.0"/>
<l c="hai" n="Haida" lng="-132.0" lat="53.0"/>
<l c="hup" n="Hupa" lng="-123.666666667" lat="41.0833333333"/>
<l c="ign" n="Ignaciano" lng="-65.4166666667" lat="-15.1666666667"/>
<l c="iva" n="Ivatan" lng="122.0" lat="20.5"/>
<l c="jaq" n="Jaqaru" lng="-76.0" lat="-13.0"/>
<l c="jeb" n="Jebero" lng="-76.5" lat="-5.41666666667"/>
<l c="jiv" n="Jivaro" lng="-78.0" lat="-2.5"/>
<l c="kab" n="Kabardian" lng="43.5" lat="43.5"/>
<l c="kgu" n="Kalkatungu" lng="139.5" lat="-21.0"/>
<l c="kay" n="Kayardild" lng="139.5" lat="-17.05"/>
<l c="klm" n="Klamath" lng="-121.5" lat="42.5"/>
<l c="koa" n="Koasati" lng="-85.1666666667" lat="34.8333333333"/>
<l c="kya" n="Kuku-Yalanji" lng="145.0" lat="-16.0"/>
<l c="kut" n="Kutenai" lng="-116.0" lat="49.5"/>
<l c="lak" n="Lak" lng="47.1666666667" lat="42.1666666667"/>
<l c="lus" n="Lushootseed" lng="-122.0" lat="48.0"/>
<l c="mal" n="Malagasy" lng="47.0" lat="-20.0"/>
<l c="mrn" n="Maranao" lng="124.25" lat="7.83333333333"/>
<l c="mrg" n="Margi" lng="13.0" lat="11.0"/>
<l c="mrt" n="Martuthunira" lng="116.5" lat="-20.8333333333"/>
<l c="maz" n="Mazahua" lng="-99.9166666667" lat="19.4166666667"/>
<l c="mbb" n="Mbabaram" lng="145.0" lat="-17.1666666667"/>
<l c="mpa" n="Murrinh-Patha" lng="129.666666667" lat="-14.6666666667"/>
<l c="nhn" n="Nahuatl (North Puebla)" lng="-98.25" lat="20.0"/>
<l c="nav" n="Navajo" lng="-108.0" lat="36.1666666667"/>
<l c="new" n="Newari (Kathmandu)" lng="85.5" lat="27.6666666667"/>
<l c="ngi" n="Ngiyambaa" lng="145.5" lat="-31.75"/>
<l c="chu" n="Nivacle" lng="-60.5" lat="-23.5"/>
<l c="nug" n="Nunggubuyu" lng="135.666666667" lat="-13.75"/>
<l c="nuu" n="Nuuchahnulth" lng="-126.666666667" lat="49.6666666667"/>
<l c="oji" n="Ojibwa (Eastern)" lng="-80.0" lat="46.0"/>
<l c="ond" n="Oneida" lng="-75.6666666667" lat="43.0"/>
<l c="pai" n="Paiwan" lng="120.833333333" lat="22.5"/>
<l c="pau" n="Paumarí" lng="-64.0" lat="-6.0"/>
<l c="prh" n="Pirahã" lng="-62.0" lat="-7.0"/>
<l c="pit" n="Pitjantjatjara" lng="130.0" lat="-26.0"/>
<l c="pae" n="Páez" lng="-76.0" lat="2.66666666667"/>
<l c="qaw" n="Qawasqar" lng="-75.0" lat="-49.0"/>
<l c="qui" n="Quileute" lng="-124.25" lat="47.9166666667"/>
<l c="ram" n="Rama" lng="-83.75" lat="11.75"/>
<l c="ruk" n="Rukai (Tanan)" lng="120.833333333" lat="22.8333333333"/>
<l c="sel" n="Selknam" lng="-70.0" lat="-53.0"/>
<l c="shs" n="Shasta" lng="-122.666666667" lat="41.8333333333"/>
<l c="shk" n="Shipibo-Konibo" lng="-75.0" lat="-7.5"/>
<l c="squ" n="Squamish" lng="-123.166666667" lat="49.6666666667"/>
<l c="tac" n="Tacana" lng="-68.0" lat="-13.5"/>
<l c="tas" n="Tashlhiyt" lng="-5.0" lat="31.0"/>
<l c="tsg" n="Tausug" lng="121.0" lat="6.0"/>
<l c="teh" n="Tehuelche" lng="-68.0" lat="-48.0"/>
<l c="tiw" n="Tiwi" lng="131.0" lat="-11.5"/>
<l c="tli" n="Tlingit" lng="-135.0" lat="59.0"/>
<l c="tpa" n="Totonac (Papantla)" lng="-97.3333333333" lat="20.3333333333"/>
<l c="tsi" n="Tsimshian (Coast)" lng="-129.0" lat="52.5"/>
<l c="wam" n="Wambaya" lng="135.75" lat="-18.6666666667"/>
<l c="wps" n="Wapishana" lng="-60.0" lat="2.66666666667"/>
<l c="wdo" n="Western Desert (Ooldea)" lng="132.0" lat="-30.5"/>
<l c="wic" n="Wichita" lng="-97.3333333333" lat="33.3333333333"/>
<l c="yny" n="Yanyuwa" lng="137.166666667" lat="-16.4166666667"/>
<l c="yes" n="Yessan-Mayo" lng="142.583333333" lat="-4.16666666667"/>
<l c="yid" n="Yidiny" lng="145.75" lat="-17.0"/>
<l c="yim" n="Yimas" lng="143.55" lat="-4.66666666667"/>
<l c="yus" n="Yupik (Siberian)" lng="-173.0" lat="65.0"/>
</v>
<v numeric="2" description="Average (5-6)" icon_id="cffffff" icon_url="https://wals.info/clld-static/icons/cffffff.png" zindex="0">
<l c="xoo" n="!Xóõ" lng="21.5" lat="-24.0"/>
<l c="ani" n="//Ani" lng="21.9166666667" lat="-18.9166666667"/>
<l c="abi" n="Abipón" lng="-61.0" lat="-29.0"/>
<l c="acm" n="Achumawi" lng="-121.0" lat="41.5"/>
<l c="ach" n="Aché" lng="-55.1666666667" lat="-25.25"/>
<l c="aco" n="Acoma" lng="-107.583333333" lat="34.9166666667"/>
<l c="aht" n="Ahtna" lng="-145.0" lat="62.0"/>
<l c="aik" n="Aikaná" lng="-60.6666666667" lat="-12.6666666667"/>
<l c="ain" n="Ainu" lng="143.0" lat="43.0"/>
<l c="ame" n="Amele" lng="145.583333333" lat="-5.25"/>
<l c="ant" n="Angaataha" lng="146.25" lat="-7.21666666667"/>
<l c="ao" n="Ao" lng="94.6666666667" lat="26.5833333333"/>
<l c="apu" n="Apurinã" lng="-67.0" lat="-9.0"/>
<l c="arb" n="Arabela" lng="-75.1666666667" lat="-2.0"/>
<l c="aeg" n="Arabic (Egyptian)" lng="31.0" lat="30.0"/>
<l c="arc" n="Archi" lng="46.8333333333" lat="42.0"/>
<l c="arm" n="Armenian (Eastern)" lng="45.0" lat="40.0"/>
<l c="asm" n="Asmat" lng="138.5" lat="-5.5"/>
<l c="ata" n="Atayal" lng="121.333333333" lat="24.5"/>
<l c="ava" n="Avar" lng="46.5" lat="42.5"/>
<l c="baj" n="Bajau (Sama)" lng="123.0" lat="-4.33333333333"/>
<l c="bsq" n="Basque" lng="-3.0" lat="43.0"/>
<l c="bto" n="Batak (Toba)" lng="99.0" lat="2.5"/>
<l c="baw" n="Bawm" lng="92.25" lat="22.5"/>
<l c="bee" n="Beembe" lng="14.0833333333" lat="-3.91666666667"/>
<l c="bej" n="Beja" lng="36.0" lat="18.0"/>
<l c="ber" n="Berta" lng="34.6666666667" lat="10.3333333333"/>
<l c="bis" n="Bisa" lng="-0.5" lat="11.5"/>
<l c="bod" n="Bodo" lng="92.0" lat="26.8333333333"/>
<l c="brh" n="Brahui" lng="67.0" lat="28.5"/>
<l c="bri" n="Bribri" lng="-83.0" lat="9.41666666667"/>
<l c="bul" n="Bulgarian" lng="25.0" lat="42.5"/>
<l c="bua" n="Burarra" lng="134.583333333" lat="-12.25"/>
<l c="bur" n="Burushaski" lng="74.5" lat="36.5"/>
<l c="cac" n="Cacua" lng="-70.0" lat="1.08333333333"/>
<l c="cam" n="Camsá" lng="-77.0" lat="1.16666666667"/>
<l c="car" n="Carib" lng="-56.0" lat="5.5"/>
<l c="cha" n="Chamorro" lng="144.75" lat="13.45"/>
<l c="cso" n="Chatino (Sierra Occidental)" lng="-97.3333333333" lat="16.25"/>
<l c="che" n="Cherokee" lng="-83.5" lat="35.5"/>
<l c="cti" n="Chin (Tiddim)" lng="93.6666666667" lat="23.3333333333"/>
<l c="cle" n="Chinantec (Lealao)" lng="-95.9166666667" lat="17.3333333333"/>
<l c="chp" n="Chipewyan" lng="-106.0" lat="59.0"/>
<l c="cve" n="Chuave" lng="145.116666667" lat="-6.11666666667"/>
<l c="chk" n="Chukchi" lng="-173.0" lat="67.0"/>
<l c="cil" n="CiLuba" lng="22.0" lat="-6.0"/>
<l c="cof" n="Cofán" lng="-77.1666666667" lat="0.166666666667"/>
<l c="cmn" n="Comanche" lng="-101.5" lat="33.5"/>
<l c="coo" n="Coos (Hanis)" lng="-124.166666667" lat="43.5"/>
<l c="cub" n="Cubeo" lng="-70.5" lat="1.33333333333"/>
<l c="dad" n="Dadibi" lng="144.583333333" lat="-6.55"/>
<l c="dag" n="Daga" lng="149.333333333" lat="-10.0"/>
<l c="dgb" n="Dagbani" lng="-0.5" lat="9.58333333333"/>
<l c="dah" n="Dahalo" lng="40.5" lat="-2.33333333333"/>
<l c="ddf" n="Daju (Dar Fur)" lng="25.25" lat="12.25"/>
<l c="dar" n="Darai" lng="84.0" lat="24.0"/>
<l c="det" n="Deti" lng="24.5" lat="-20.5"/>
<l c="die" n="Diegueño (Mesa Grande)" lng="-116.166666667" lat="32.6666666667"/>
<l c="diz" n="Dizi" lng="36.5" lat="6.16666666667"/>
<l c="der" n="Dla (Proper)" lng="141.0" lat="-3.58333333333"/>
<l c="eka" n="Ekari" lng="135.5" lat="-3.83333333333"/>
<l c="evn" n="Even" lng="130.0" lat="68.0"/>
<l c="eve" n="Evenki" lng="125.0" lat="56.0"/>
<l c="fas" n="Fasu" lng="143.333333333" lat="-6.58333333333"/>
<l c="fij" n="Fijian" lng="178.0" lat="-17.8333333333"/>
<l c="fur" n="Fur" lng="25.0" lat="13.5"/>
<l c="fye" n="Fyem" lng="9.33333333333" lat="9.58333333333"/>
<l c="gar" n="Garo" lng="90.5" lat="25.6666666667"/>
<l c="geo" n="Georgian" lng="44.0" lat="42.0"/>
<l c="goa" n="Goajiro" lng="-72.0" lat="12.0"/>
<l c="grk" n="Greek (Modern)" lng="22.0" lat="39.0"/>
<l c="ghb" n="Guahibo" lng="-69.0" lat="5.0"/>
<l c="gmb" n="Guambiano" lng="-76.6666666667" lat="2.5"/>
<l c="gua" n="Guaraní" lng="-56.0" lat="-26.0"/>
<l c="gwa" n="Gwari" lng="7.0" lat="9.5"/>
<l c="had" n="Hadza" lng="35.1666666667" lat="-3.75"/>
<l c="hak" n="Hakka" lng="116.0" lat="25.0"/>
<l c="hmr" n="Hamer" lng="36.5" lat="5.0"/>
<l c="hau" n="Hausa" lng="7.0" lat="12.0"/>
<l c="haw" n="Hawaiian" lng="-155.5" lat="19.5833333333"/>
<l c="hba" n="Hebrew (Modern Ashkenazic)" lng="35.1666666667" lat="31.75"/>
<l c="hin" n="Hindi" lng="77.0" lat="25.0"/>
<l c="hix" n="Hixkaryana" lng="-59.0" lat="-1.0"/>
<l c="hmo" n="Hmong Njua" lng="105.0" lat="28.0"/>
<l c="hop" n="Hopi" lng="-110.0" lat="36.0"/>
<l c="htc" n="Huastec" lng="-99.3333333333" lat="22.0833333333"/>
<l c="hve" n="Huave (San Mateo del Mar)" lng="-95.0" lat="16.2166666667"/>
<l c="hum" n="Huitoto (Murui)" lng="-73.5" lat="-1.0"/>
<l c="iba" n="Iban" lng="112.0" lat="2.0"/>
<l c="ind" n="Indonesian" lng="106.0" lat="0.0"/>
<l c="igs" n="Ingessana" lng="34.0" lat="11.5"/>
<l c="ing" n="Ingush" lng="45.0833333333" lat="43.1666666667"/>
<l c="irx" n="Iranxe" lng="-58.0" lat="-13.0"/>
<l c="irq" n="Iraqw" lng="35.5" lat="-4.0"/>
<l c="ird" n="Irish (Donegal)" lng="-8.0" lat="55.0"/>
<l c="ite" n="Itelmen" lng="157.5" lat="57.0"/>
<l c="ito" n="Itonama" lng="-64.3333333333" lat="-12.8333333333"/>
<l c="iwm" n="Iwam" lng="142.0" lat="-4.33333333333"/>
<l c="jak" n="Jakaltek" lng="-91.6666666667" lat="15.6666666667"/>
<l c="jpn" n="Japanese" lng="140.0" lat="37.0"/>
<l c="jpr" n="Japreria" lng="-73.0" lat="10.5"/>
<l c="jng" n="Jingpho" lng="97.0" lat="25.4166666667"/>
<l c="juh" n="Ju|&#39;hoan" lng="21.0" lat="-19.0"/>
<l c="kek" n="K&#39;ekchí" lng="-89.8333333333" lat="16.0"/>
<l c="kad" n="Kadugli" lng="29.6666666667" lat="11.0"/>
<l c="kly" n="Kala Lagaw Ya" lng="142.116666667" lat="-10.1166666667"/>
<l c="kal" n="Kalami" lng="72.5" lat="35.5"/>
<l c="knk" n="Kanakuru" lng="12.0" lat="10.0"/>
<l c="knd" n="Kannada" lng="76.0" lat="14.0"/>
<l c="krk" n="Karok" lng="-123.0" lat="41.6666666667"/>
<l c="kws" n="Kawaiisu" lng="-117.5" lat="36.0"/>
<l c="ked" n="Kedang" lng="123.75" lat="-8.25"/>
<l c="kef" n="Kefa" lng="36.25" lat="7.25"/>
<l c="ker" n="Kera" lng="15.0833333333" lat="9.83333333333"/>
<l c="kew" n="Kewa" lng="143.833333333" lat="-6.5"/>
<l c="kty" n="Khanty" lng="65.0" lat="65.0"/>
<l c="khr" n="Kharia" lng="84.3333333333" lat="22.5"/>
<l c="khs" n="Khasi" lng="92.0" lat="25.5"/>
<l c="klv" n="Kilivila" lng="151.083333333" lat="-8.5"/>
<l c="kio" n="Kiowa" lng="-99.0" lat="37.0"/>
<l c="krb" n="Kiribati" lng="173.0" lat="1.33333333333"/>
<l c="kiw" n="Kiwai (Southern)" lng="143.5" lat="-8.0"/>
<l c="koi" n="Koiari" lng="147.333333333" lat="-9.5"/>
<l c="kry" n="Koryak" lng="167.0" lat="61.0"/>
<l c="kot" n="Kota" lng="77.1666666667" lat="11.5"/>
<l c="koy" n="Koya" lng="81.3333333333" lat="17.5"/>
<l c="kch" n="Koyra Chiini" lng="-3.0" lat="17.0"/>
<l c="kse" n="Koyraboro Senni" lng="0.0" lat="16.0"/>
<l c="kpa" n="Kpan" lng="10.1666666667" lat="7.58333333333"/>
<l c="kul" n="Kullo" lng="37.0833333333" lat="6.75"/>
<l c="kun" n="Kuna" lng="-77.3333333333" lat="8.0"/>
<l c="knm" n="Kunama" lng="37.0" lat="14.5"/>
<l c="kmp" n="Kunimaipa" lng="146.833333333" lat="-8.0"/>
<l c="kur" n="Kurukh" lng="85.5" lat="22.8333333333"/>
<l c="kwa" n="Kwaio" lng="161.0" lat="-8.95"/>
<l c="kwk" n="Kwakw&#39;ala" lng="-127.0" lat="51.0"/>
<l c="lad" n="Ladakhi" lng="78.0" lat="34.0"/>
<l c="lkt" n="Lakhota" lng="-101.833333333" lat="43.8333333333"/>
<l c="lkk" n="Lakkia" lng="110.166666667" lat="24.0833333333"/>
<l c="lam" n="Lamé" lng="14.5" lat="9.0"/>
<l c="lat" n="Latvian" lng="24.0" lat="57.0"/>
<l c="lav" n="Lavukaleve" lng="159.2" lat="-9.08333333333"/>
<l c="len" n="Lenakel" lng="169.25" lat="-19.45"/>
<l c="lez" n="Lezgian" lng="47.8333333333" lat="41.6666666667"/>
<l c="lit" n="Lithuanian" lng="24.0" lat="55.0"/>
<l c="lui" n="Luiseño" lng="-117.166666667" lat="33.3333333333"/>
<l c="kkv" n="Lusi" lng="149.666666667" lat="-5.58333333333"/>
<l c="luv" n="Luvale" lng="22.0" lat="-12.0"/>
<l c="mya" n="Ma&#39;ya" lng="130.916666667" lat="-1.25"/>
<l c="mne" n="Maidu (Northeast)" lng="-120.666666667" lat="40.0"/>
<l c="mak" n="Makah" lng="-124.666666667" lat="48.3333333333"/>
<l c="mlk" n="Malakmalak" lng="130.416666667" lat="-13.4166666667"/>
<l c="mnc" n="Manchu" lng="127.5" lat="49.5"/>
<l c="mnd" n="Mandarin" lng="110.0" lat="34.0"/>
<l c="myi" n="Mangarrayi" lng="133.5" lat="-14.6666666667"/>
<l c="mgg" n="Mangghuer" lng="102.0" lat="36.0"/>
<l c="mao" n="Maori" lng="176.0" lat="-40.0"/>
<l c="map" n="Mapudungun" lng="-72.0" lat="-38.0"/>
<l c="mku" n="Maranungku" lng="130.0" lat="-13.6666666667"/>
<l c="mar" n="Maricopa" lng="-113.166666667" lat="33.1666666667"/>
<l c="mrd" n="Marind" lng="140.166666667" lat="-7.83333333333"/>
<l c="mau" n="Maung" lng="133.5" lat="-11.9166666667"/>
<l c="max" n="Maxakalí" lng="-40.0" lat="-18.0"/>
<l c="may" n="Maybrat" lng="132.5" lat="-1.33333333333"/>
<l c="mzc" n="Mazatec (Chiquihuitlán)" lng="-96.9166666667" lat="17.75"/>
<l c="mei" n="Meithei" lng="94.0" lat="24.75"/>
<l c="hok" n="Min (Southern)" lng="118.0" lat="25.0"/>
<l c="mss" n="Miwok (Southern Sierra)" lng="-120.0" lat="37.5"/>
<l c="mxc" n="Mixtec (Chalcatongo)" lng="-97.5833333333" lat="17.05"/>
<l c="mxm" n="Mixtec (Molinos)" lng="-97.5833333333" lat="17.0"/>
<l c="mog" n="Moghol" lng="62.0" lat="35.0"/>
<l c="mor" n="Mor" lng="135.75" lat="-2.95"/>
<l c="mov" n="Movima" lng="-65.6666666667" lat="-13.8333333333"/>
<l c="mui" n="Muinane" lng="-72.5" lat="-1.0"/>
<l c="mum" n="Mumuye" lng="11.6666666667" lat="9.0"/>
<l c="mun" n="Mundari" lng="84.6666666667" lat="23.0"/>
<l c="nht" n="Nahuatl (Tetelcingo)" lng="-99.0" lat="19.6666666667"/>
<l c="kho" n="Nama" lng="18.0" lat="-25.5"/>
<l c="nmb" n="Nambikuára (Southern)" lng="-59.5" lat="-14.0"/>
<l c="nai" n="Nanai" lng="137.0" lat="49.5"/>
<l c="nar" n="Nara (in Ethiopia)" lng="37.5833333333" lat="15.0833333333"/>
<l c="nas" n="Nasioi" lng="155.583333333" lat="-6.33333333333"/>
<l c="ndy" n="Ndyuka" lng="-54.5" lat="4.5"/>
<l c="ntu" n="Nenets" lng="76.0" lat="70.0"/>
<l c="nap" n="Neo-Aramaic (Persian Azerbaijan)" lng="47.0" lat="38.0"/>
<l c="nep" n="Nepali" lng="85.0" lat="28.0"/>
<l c="nez" n="Nez Perce" lng="-116.0" lat="46.0"/>
<l c="ngz" n="Ngizim" lng="10.9166666667" lat="12.0833333333"/>
<l c="nim" n="Nimboran" lng="140.166666667" lat="-2.5"/>
<l c="niv" n="Nivkh" lng="142.0" lat="53.3333333333"/>
<l c="nko" n="Nkore-Kiga" lng="29.8333333333" lat="-0.916666666667"/>
<l c="nob" n="Nobiin" lng="31.0" lat="21.0"/>
<l c="nun" n="Nung (in Vietnam)" lng="106.416666667" lat="21.9166666667"/>
<l c="ood" n="O&#39;odham" lng="-112.0" lat="32.0"/>
<l c="oca" n="Ocaina" lng="-71.75" lat="-2.75"/>
<l c="orm" n="Ormuri" lng="69.75" lat="32.5"/>
<l c="orh" n="Oromo (Harar)" lng="42.0" lat="9.0"/>
<l c="pms" n="Paamese" lng="168.25" lat="-16.5"/>
<l c="psh" n="Pashto" lng="67.0" lat="33.0"/>
<l c="psm" n="Passamaquoddy-Maliseet" lng="-67.0" lat="45.0"/>
<l c="paw" n="Pawaian" lng="145.083333333" lat="-7.0"/>
<l c="pec" n="Pech" lng="-85.5" lat="15.0"/>
<l c="prs" n="Persian" lng="54.0" lat="32.0"/>
<l c="pol" n="Polish" lng="20.0" lat="52.0"/>
<l c="pso" n="Pomo (Southeastern)" lng="-122.5" lat="39.0"/>
<l c="pur" n="Purépecha" lng="-101.666666667" lat="19.5"/>
<l c="bng" n="Qaqet" lng="152.0" lat="-4.58333333333"/>
<l c="qco" n="Quechua (Cochabamba)" lng="-66.0" lat="-17.5"/>
<l c="rap" n="Rapanui" lng="-109.366666667" lat="-27.1166666667"/>
<l c="res" n="Resígaro" lng="-71.5" lat="-2.41666666667"/>
<l c="rsc" n="Romansch (Scharans)" lng="9.5" lat="46.75"/>
<l c="ror" n="Roro" lng="146.583333333" lat="-8.75"/>
<l c="rtk" n="Rotokas" lng="155.166666667" lat="-6.0"/>
<l c="rus" n="Russian" lng="38.0" lat="56.0"/>
<l c="rut" n="Rutul" lng="47.4166666667" lat="41.5"/>
<l c="scs" n="Saami (Central-South)" lng="16.75" lat="64.6666666667"/>
<l c="sdw" n="Sandawe" lng="35.0" lat="-5.0"/>
<l c="svs" n="Savosavo" lng="159.8" lat="-9.13333333333"/>
<l c="seb" n="Sebei" lng="34.5833333333" lat="1.33333333333"/>
<l c="slp" n="Selepet" lng="147.166666667" lat="-6.16666666667"/>
<l c="snc" n="Seneca" lng="-77.5" lat="42.5"/>
<l c="sha" n="Shan" lng="98.0" lat="22.0"/>
<l c="shi" n="Shiriana" lng="-62.8333333333" lat="3.5"/>
<l c="shu" n="Shuswap" lng="-120.0" lat="52.0"/>
<l c="sin" n="Siona" lng="-76.25" lat="0.333333333333"/>
<l c="sla" n="Slave" lng="-125.0" lat="67.0"/>
<l c="soq" n="Soqotri" lng="54.0" lat="12.5"/>
<l c="sor" n="Sora" lng="84.3333333333" lat="20.0"/>
<l c="spa" n="Spanish" lng="-4.0" lat="40.0"/>
<l c="sue" n="Suena" lng="147.55" lat="-7.75"/>
<l c="swa" n="Swahili" lng="39.0" lat="-6.5"/>
<l c="sba" n="Sáliba (in Colombia)" lng="-70.0" lat="6.0"/>
<l c="tab" n="Taba" lng="127.5" lat="0.0"/>
<l c="tag" n="Tagalog" lng="121.0" lat="15.0"/>
<l c="tam" n="Tamang (Eastern)" lng="85.666666666667" lat="27.5"/>
<l c="tok" n="Tarok" lng="10.0833333333" lat="9.0"/>
<l c="tel" n="Telugu" lng="79.0" lat="16.0"/>
<l c="ter" n="Tera" lng="11.8333333333" lat="11.0"/>
<l c="ttn" n="Tetun" lng="126.0" lat="-9.0"/>
<l c="tic" n="Ticuna" lng="-70.5" lat="-4.0"/>
<l c="tgk" n="Tigak" lng="150.8" lat="-2.71666666667"/>
<l c="tgr" n="Tigré" lng="38.5" lat="16.5"/>
<l c="try" n="Tiruray" lng="124.166666667" lat="6.75"/>
<l c="twn" n="Tiwa (Northern)" lng="-105.5" lat="36.5"/>
<l c="toa" n="Toaripi" lng="146.25" lat="-8.33333333333"/>
<l c="tol" n="Tol" lng="-87.0" lat="14.6666666667"/>
<l c="ton" n="Tonkawa" lng="-96.75" lat="30.25"/>
<l c="tru" n="Trumai" lng="-53.5833333333" lat="-11.9166666667"/>
<l c="tso" n="Tsou" lng="120.75" lat="23.5"/>
<l c="ttu" n="Tsova-Tush" lng="45.5" lat="42.5"/>
<l c="tuk" n="Tukang Besi" lng="123.5" lat="-5.5"/>
<l c="tza" n="Tzeltal (Aguacatenango)" lng="-92.5" lat="16.4166666667"/>
<l c="umb" n="UMbundu" lng="15.0" lat="-12.5"/>
<l c="ung" n="Ungarinjin" lng="126.0" lat="-16.3333333333"/>
<l c="urk" n="Urubú-Kaapor" lng="-46.5" lat="-2.33333333333"/>
<l c="usa" n="Usan" lng="145.166666667" lat="-4.83333333333"/>
<l c="uzn" n="Uzbek (Northern)" lng="66.5" lat="40.6666666667"/>
<l c="wah" n="Wahgi" lng="144.716666667" lat="-5.83333333333"/>
<l c="bno" n="Waimaha" lng="-70.25" lat="0.333333333333"/>
<l c="wao" n="Waorani" lng="-76.5" lat="-1.0"/>
<l c="wap" n="Wappo" lng="-122.5" lat="38.5"/>
<l c="wra" n="Warao" lng="-61.6666666667" lat="9.33333333333"/>
<l c="wry" n="Waray (in Australia)" lng="131.25" lat="-13.1666666667"/>
<l c="wrd" n="Wardaman" lng="131.0" lat="-15.5"/>
<l c="war" n="Wari&#39;" lng="-65.0" lat="-11.3333333333"/>
<l c="wma" n="West Makian" lng="127.583333333" lat="0.5"/>
<l c="wch" n="Wichí" lng="-62.5833333333" lat="-22.5"/>
<l c="wmu" n="Wik Munkan" lng="141.75" lat="-13.9166666667"/>
<l c="win" n="Wintu" lng="-122.5" lat="41.0"/>
<l c="wiy" n="Wiyot" lng="-124.166666667" lat="40.8333333333"/>
<l c="ygr" n="Yagaria" lng="145.416666667" lat="-6.33333333333"/>
<l c="yag" n="Yagua" lng="-72.0" lat="-3.5"/>
<l c="yan" n="Yana" lng="-122.0" lat="40.5"/>
<l c="yaq" n="Yaqui" lng="-110.25" lat="27.5"/>
<l c="yar" n="Yareba" lng="148.5" lat="-9.5"/>
<l c="yaw" n="Yawa" lng="136.25" lat="-1.75"/>
<l c="yay" n="Yay" lng="104.75" lat="22.4166666667"/>
<l c="yey" n="Yeyi" lng="23.5" lat="-20.0"/>
<l c="yct" n="Yucatec" lng="-89.0" lat="20.0"/>
<l c="yuc" n="Yuchi" lng="-86.75" lat="35.75"/>
<l c="ycn" n="Yucuna" lng="-71.0" lat="-0.75"/>
<l c="yko" n="Yukaghir (Kolyma)" lng="150.833333333" lat="65.75"/>
<l c="ytu" n="Yukaghir (Tundra)" lng="155.0" lat="69.0"/>
<l c="yur" n="Yurok" lng="-124.0" lat="41.3333333333"/>
<l c="zqc" n="Zoque (Copainalá)" lng="-93.25" lat="17.0"/>
<l c="zul" n="Zulu" lng="30.0" lat="-30.0"/>
<l c="zun" n="Zuni" lng="-108.833333333" lat="35.0833333333"/>
</v>
<v numeric="3" description="Large (7-14)" icon_id="cdd0000" icon_url="https://wals.info/clld-static/icons/cdd0000.png" zindex="0">
<l c="agh" n="Aghem" lng="10.0" lat="6.66666666667"/>
<l c="aiz" n="Aizi" lng="-4.5" lat="5.25"/>
<l c="akn" n="Akan" lng="-1.25" lat="6.5"/>
<l c="akw" n="Akawaio" lng="-59.5" lat="6.0"/>
<l c="ala" n="Alamblak" lng="143.333333333" lat="-4.66666666667"/>
<l c="alb" n="Albanian" lng="20.0" lat="41.0"/>
<l c="ald" n="Alladian" lng="-4.33333333333" lat="5.16666666667"/>
<l c="amh" n="Amharic" lng="38.0" lat="10.0"/>
<l c="amo" n="Amo" lng="8.66666666667" lat="10.3333333333"/>
<l c="amz" n="Amuzgo" lng="-98.0" lat="16.8333333333"/>
<l c="adk" n="Andoke" lng="-72.0" lat="-0.666666666667"/>
<l c="anc" n="Angas" lng="9.5" lat="9.5"/>
<l c="api" n="Apinayé" lng="-48.0" lat="-5.5"/>
<l c="arp" n="Arapesh (Mountain)" lng="143.166666667" lat="-3.46666666667"/>
<l c="awn" n="Awngi" lng="36.6666666667" lat="10.8333333333"/>
<l c="aze" n="Azerbaijani" lng="48.5" lat="40.5"/>
<l c="bag" n="Bagirmi" lng="16.0" lat="11.6666666667"/>
<l c="bai" n="Bai" lng="100.0" lat="26.0"/>
<l c="bki" n="Bakairí" lng="-55.0" lat="-14.0"/>
<l c="bam" n="Bambara" lng="-7.5" lat="12.5"/>
<l c="brb" n="Bariba" lng="2.5" lat="10.0"/>
<l c="bsk" n="Bashkir" lng="58.0" lat="53.0"/>
<l c="bkr" n="Batak (Karo)" lng="98.25" lat="3.25"/>
<l c="ben" n="Bengali" lng="90.0" lat="24.0"/>
<l c="bir" n="Birom" lng="8.83333333333" lat="9.66666666667"/>
<l c="bbf" n="Bobo Madaré (Northern)" lng="-4.3333333333333" lat="12.4166666666667"/>
<l c="brr" n="Bororo" lng="-57.0" lat="-16.0"/>
<l c="bra" n="Brao" lng="107.5" lat="14.1666666667"/>
<l c="bre" n="Breton" lng="-3.0" lat="48.0"/>
<l c="brw" n="Bru (Western)" lng="104.75" lat="16.75"/>
<l c="brm" n="Burmese" lng="96.0" lat="21.0"/>
<l c="bet" n="Bété" lng="-6.25" lat="6.25"/>
<l c="cnl" n="Canela" lng="-45.0" lat="-7.0"/>
<l c="cnt" n="Cantonese" lng="113.0" lat="23.0"/>
<l c="ctl" n="Catalan" lng="2.0" lat="41.75"/>
<l c="cyv" n="Cayuvava" lng="-65.5" lat="-13.5"/>
<l c="chw" n="Cham (Western)" lng="105.5" lat="12.0"/>
<l c="chq" n="Chinantec (Quiotepec)" lng="-96.6666666667" lat="17.5833333333"/>
<l c="chv" n="Chuvash" lng="47.5" lat="55.5"/>
<l c="dgr" n="Dagur" lng="124.0" lat="48.0"/>
<l c="dan" n="Dan" lng="-8.0" lat="7.5"/>
<l c="dnw" n="Dangaléat (Western)" lng="18.3333333333" lat="12.1666666667"/>
<l c="dni" n="Dani (Lower Grand Valley)" lng="138.833333333" lat="-4.33333333333"/>
<l c="din" n="Dinka" lng="28.0" lat="8.5"/>
<l c="dio" n="Diola-Fogny" lng="-16.25" lat="13.0"/>
<l c="don" n="Dong (Southern)" lng="109.0" lat="27.0"/>
<l c="doy" n="Doyayo" lng="13.0833333333" lat="8.66666666667"/>
<l c="dre" n="Drehu" lng="167.25" lat="-21.0"/>
<l c="dum" n="Dumo" lng="141.3" lat="-2.68333333333"/>
<l c="efi" n="Efik" lng="8.5" lat="4.91666666667"/>
<l c="eja" n="Ejagham" lng="8.66666666667" lat="5.41666666667"/>
<l c="eng" n="English" lng="0.0" lat="52.0"/>
<l c="epe" n="Epena Pedee" lng="-77.0" lat="3.0"/>
<l c="ewe" n="Ewe" lng="0.416666666667" lat="6.33333333333"/>
<l c="ewo" n="Ewondo" lng="12.0" lat="4.0"/>
<l c="fef" n="Fe&#39;fe&#39;" lng="10.1666666667" lat="5.25"/>
<l c="fin" n="Finnish" lng="25.0" lat="62.0"/>
<l c="fre" n="French" lng="2.0" lat="48.0"/>
<l c="ful" n="Fulniô" lng="-37.5" lat="-8.0"/>
<l c="fuz" n="Fuzhou" lng="119.5" lat="26.0"/>
<l c="gbb" n="Gbeya Bossangoa" lng="17.5" lat="6.66666666667"/>
<l c="gla" n="Gelao" lng="105.5" lat="22.9166666667"/>
<l c="ger" n="German" lng="10.0" lat="52.0"/>
<l c="gan" n="Great Andamanese" lng="92.6666666667" lat="12.0"/>
<l c="grb" n="Grebo" lng="-8.0" lat="5.0"/>
<l c="ga" n="Gã" lng="-0.166666666667" lat="5.66666666667"/>
<l c="ham" n="Hamtai" lng="146.25" lat="-7.5"/>
<l c="hun" n="Hungarian" lng="20.0" lat="47.0"/>
<l c="hzb" n="Hunzib" lng="46.25" lat="42.1666666667"/>
<l c="iaa" n="Iaai" lng="166.583333333" lat="-20.4166666667"/>
<l c="igb" n="Igbo" lng="7.33333333333" lat="6.0"/>
<l c="ijo" n="Ijo (Kolokuma)" lng="5.66666666667" lat="4.91666666667"/>
<l c="ik" n="Ik" lng="34.1666666667" lat="3.75"/>
<l c="ika" n="Ika" lng="-73.75" lat="10.6666666667"/>
<l c="imo" n="Imonda" lng="141.166666667" lat="-3.33333333333"/>
<l c="irr" n="Irarutu" lng="133.5" lat="-3.0"/>
<l c="iso" n="Isoko" lng="6.25" lat="5.5"/>
<l c="jav" n="Javanese" lng="111.0" lat="-7.0"/>
<l c="jeh" n="Jeh" lng="107.833333333" lat="15.1666666667"/>
<l c="jom" n="Jomang" lng="30.5" lat="10.5833333333"/>
<l c="kng" n="Kaingang" lng="-52.0" lat="-26.0"/>
<l c="knr" n="Kanuri" lng="13.0" lat="12.0"/>
<l c="ksg" n="Karen (Sgaw)" lng="97.0" lat="18.0"/>
<l c="kas" n="Kashmiri" lng="76.0" lat="34.0"/>
<l c="kyl" n="Kayah Li (Eastern)" lng="97.5" lat="19.0"/>
<l c="ket" n="Ket" lng="87.0" lat="64.0"/>
<l c="kha" n="Khalkha" lng="105.0" lat="47.0"/>
<l c="khm" n="Khmer" lng="105.0" lat="12.5"/>
<l c="kmu" n="Khmu&#39;" lng="102.0" lat="21.0"/>
<l c="kgz" n="Kirghiz" lng="75.0" lat="42.0"/>
<l c="kss" n="Kisi (Southern)" lng="-10.25" lat="8.5"/>
<l c="kla" n="Klao" lng="-8.75" lat="4.75"/>
<l c="kob" n="Kobon" lng="144.333333333" lat="-5.16666666667"/>
<l c="koh" n="Kohumono" lng="8.11666666667" lat="6.0"/>
<l c="kzy" n="Komi-Zyrian" lng="55.0" lat="65.0"/>
<l c="kom" n="Komo" lng="33.75" lat="8.75"/>
<l c="kkn" n="Konkani" lng="74.0" lat="15.25"/>
<l c="kor" n="Korean" lng="128.0" lat="37.5"/>
<l c="kfe" n="Koromfe" lng="-0.916666666667" lat="14.25"/>
<l c="ktk" n="Kotoko" lng="15.3333333333" lat="11.3333333333"/>
<l c="kpe" n="Kpelle" lng="-10.0" lat="7.0"/>
<l c="kro" n="Krongo" lng="30.0" lat="10.5"/>
<l c="krd" n="Kurdish (Central)" lng="44.0" lat="36.0"/>
<l c="kwo" n="Kwoma" lng="142.75" lat="-4.16666666667"/>
<l c="lah" n="Lahu" lng="98.1666666667" lat="20.0"/>
<l c="lan" n="Lango" lng="33.0" lat="2.16666666667"/>
<l c="llm" n="Lelemi" lng="0.5" lat="7.33333333333"/>
<l c="lep" n="Lepcha" lng="88.5" lat="27.1666666667"/>
<l c="lua" n="Lua" lng="17.75" lat="9.75"/>
<l c="lug" n="Lugbara" lng="30.9166666667" lat="3.08333333333"/>
<l c="luo" n="Luo" lng="34.75" lat="-0.5"/>
<l c="lu" n="Lü" lng="100.666666667" lat="22.0"/>
<l c="maa" n="Maasai" lng="36.0" lat="-3.0"/>
<l c="mab" n="Maba" lng="20.8333333333" lat="13.75"/>
<l c="mla" n="Mambila" lng="11.5" lat="6.75"/>
<l c="mme" n="Mari (Meadow)" lng="48.0" lat="57.0"/>
<l c="mba" n="Mba" lng="25.0" lat="1.0"/>
<l c="mie" n="Mien" lng="111.0" lat="25.0"/>
<l c="mtp" n="Mixe (Totontepec)" lng="-96.0" lat="17.25"/>
<l c="mro" n="Moro" lng="30.1666666667" lat="11.0"/>
<l c="mrl" n="Murle" lng="33.5" lat="6.5"/>
<l c="nnc" n="Nancowry" lng="93.5" lat="8.05"/>
<l c="nan" n="Nandi" lng="35.0" lat="0.25"/>
<l c="nbk" n="Natügu" lng="165.866666667" lat="-10.7833333333"/>
<l c="nax" n="Naxi" lng="100.0" lat="27.5"/>
<l c="ndt" n="Ndut" lng="-16.9166666667" lat="14.9166666667"/>
<l c="nga" n="Nganasan" lng="93.0" lat="71.0"/>
<l c="nti" n="Ngiti" lng="30.25" lat="1.33333333333"/>
<l c="non" n="Noni" lng="10.5833333333" lat="6.41666666667"/>
<l c="nor" n="Norwegian" lng="8.0" lat="61.0"/>
<l c="nkt" n="Nyah Kur (Tha Pong)" lng="101.666666667" lat="15.6666666667"/>
<l c="nyg" n="Nyangi" lng="33.5833333333" lat="3.41666666667"/>
<l c="nyi" n="Nyimang" lng="29.3333333333" lat="12.1666666667"/>
<l c="nis" n="Nyishi" lng="93.5" lat="27.5"/>
<l c="ogb" n="Ogbia" lng="6.25" lat="4.66666666667"/>
<l c="otm" n="Otomí (Mezquital)" lng="-99.1666666667" lat="20.1666666667"/>
<l c="pac" n="Pacoh" lng="107.083333333" lat="16.4166666667"/>
<l c="pnr" n="Panare" lng="-66.0" lat="6.5"/>
<l c="puk" n="Parauk" lng="99.5" lat="23.25"/>
<l c="phl" n="Phlong" lng="99.0" lat="15.0"/>
<l c="poa" n="Po-Ai" lng="164.833333333" lat="-20.6666666667"/>
<l c="poh" n="Pohnpeian" lng="158.25" lat="6.88333333333"/>
<l c="rom" n="Romanian" lng="25.0" lat="46.0"/>
<l c="sab" n="Sa&#39;ban" lng="115.666666667" lat="3.66666666667"/>
<l c="san" n="Sango" lng="18.0" lat="5.0"/>
<l c="snm" n="Sanuma" lng="-64.6666666667" lat="4.5"/>
<l c="sed" n="Sedang" lng="108.0" lat="14.8333333333"/>
<l c="skp" n="Selkup" lng="82.0" lat="65.0"/>
<l c="sml" n="Semelai" lng="103.0" lat="3.0"/>
<l c="snd" n="Senadi" lng="-6.25" lat="9.5"/>
<l c="snt" n="Sentani" lng="140.583333333" lat="-2.58333333333"/>
<l c="sdh" n="Sindhi" lng="69.0" lat="26.0"/>
<l c="snh" n="Sinhala" lng="80.5" lat="7.0"/>
<l c="srn" n="Sirionó" lng="-64.0" lat="-15.5833333333"/>
<l c="som" n="Somali" lng="45.0" lat="3.0"/>
<l c="sre" n="Sre" lng="108.0" lat="11.5"/>
<l c="sui" n="Sui" lng="107.5" lat="26.0"/>
<l c="sup" n="Supyire" lng="-5.58333333333" lat="11.5"/>
<l c="tma" n="Tama" lng="22.0" lat="14.5"/>
<l c="tmp" n="Tampulma" lng="-0.583333333333" lat="10.4166666667"/>
<l c="tks" n="Teke (Southern)" lng="14.5" lat="-2.33333333333"/>
<l c="tmn" n="Temein" lng="29.4166666667" lat="11.9166666667"/>
<l c="tne" n="Temne" lng="-13.0833333333" lat="8.66666666667"/>
<l c="tha" n="Thai" lng="101.0" lat="16.0"/>
<l c="tib" n="Tibetan (Standard Spoken)" lng="91.0" lat="30.0"/>
<l c="dts" n="Toro So" lng="-3.25" lat="14.4166666667"/>
<l c="tug" n="Tuareg (Ahaggar)" lng="6.0" lat="23.0"/>
<l c="tul" n="Tulu" lng="75.3333333333" lat="12.75"/>
<l c="tun" n="Tunica" lng="-91.0" lat="32.6666666667"/>
<l c="tur" n="Turkish" lng="35.0" lat="39.0"/>
<l c="tuv" n="Tuvan" lng="95.0" lat="52.0"/>
<l c="una" n="Una" lng="140.0" lat="-4.66666666667"/>
<l c="vie" n="Vietnamese" lng="106.5" lat="10.5"/>
<l c="wnt" n="Wantoat" lng="146.5" lat="-6.16666666667"/>
<l c="wrs" n="Waris" lng="141.0" lat="-3.16666666667"/>
<l c="woi" n="Woisika" lng="124.833333333" lat="-8.25"/>
<l c="wlf" n="Wolof" lng="-16.0" lat="15.25"/>
<l c="wuc" n="Wu" lng="119.916666667" lat="31.6666666667"/>
<l c="ykt" n="Yakut" lng="130.0" lat="62.0"/>
<l c="yap" n="Yapese" lng="138.166666667" lat="9.58333333333"/>
<l c="yel" n="Yelî Dnye" lng="154.166666667" lat="-11.3666666667"/>
<l c="yor" n="Yoruba" lng="4.33333333333" lat="8.0"/>
<l c="yul" n="Yulu" lng="25.25" lat="8.5"/>
<l c="zan" n="Zande" lng="26.0" lat="4.0"/>
</v>
</feature>
"""

WALS_18A_CONSONANT_ABSENCES = """
<feature number="18A" base_url="https://wals.info/" name="Absence of Common Consonants">
<description>
<url>https://wals.info/feature/18A.xml</url>
<timestamp>2024-10-18T11:59:12.029308+02:00</timestamp>
</description>
<v numeric="1" description="All present" icon_id="cffffff" icon_url="https://wals.info/clld-static/icons/cffffff.png" zindex="0">
<l c="xoo" n="!Xóõ" lng="21.5" lat="-24.0"/>
<l c="ani" n="//Ani" lng="21.9166666667" lat="-18.9166666667"/>
<l c="abi" n="Abipón" lng="-61.0" lat="-29.0"/>
<l c="abk" n="Abkhaz" lng="41.0" lat="43.0833333333"/>
<l c="acm" n="Achumawi" lng="-121.0" lat="41.5"/>
<l c="ach" n="Aché" lng="-55.1666666667" lat="-25.25"/>
<l c="aco" n="Acoma" lng="-107.583333333" lat="34.9166666667"/>
<l c="adz" n="Adzera" lng="146.25" lat="-6.25"/>
<l c="agh" n="Aghem" lng="10.0" lat="6.66666666667"/>
<l c="aht" n="Ahtna" lng="-145.0" lat="62.0"/>
<l c="aik" n="Aikaná" lng="-60.6666666667" lat="-12.6666666667"/>
<l c="ain" n="Ainu" lng="143.0" lat="43.0"/>
<l c="aiz" n="Aizi" lng="-4.5" lat="5.25"/>
<l c="akn" n="Akan" lng="-1.25" lat="6.5"/>
<l c="akw" n="Akawaio" lng="-59.5" lat="6.0"/>
<l c="abm" n="Alabama" lng="-87.4166666667" lat="32.3333333333"/>
<l c="ala" n="Alamblak" lng="143.333333333" lat="-4.66666666667"/>
<l c="alb" n="Albanian" lng="20.0" lat="41.0"/>
<l c="aea" n="Aleut (Eastern)" lng="-164.0" lat="54.75"/>
<l c="ald" n="Alladian" lng="-4.33333333333" lat="5.16666666667"/>
<l c="amc" n="Amahuaca" lng="-72.5" lat="-10.5"/>
<l c="ame" n="Amele" lng="145.583333333" lat="-5.25"/>
<l c="amh" n="Amharic" lng="38.0" lat="10.0"/>
<l c="amo" n="Amo" lng="8.66666666667" lat="10.3333333333"/>
<l c="amu" n="Amuesha" lng="-75.4166666667" lat="-10.5"/>
<l c="amz" n="Amuzgo" lng="-98.0" lat="16.8333333333"/>
<l c="anc" n="Angas" lng="9.5" lat="9.5"/>
<l c="ao" n="Ao" lng="94.6666666667" lat="26.5833333333"/>
<l c="api" n="Apinayé" lng="-48.0" lat="-5.5"/>
<l c="apu" n="Apurinã" lng="-67.0" lat="-9.0"/>
<l c="arb" n="Arabela" lng="-75.1666666667" lat="-2.0"/>
<l c="aeg" n="Arabic (Egyptian)" lng="31.0" lat="30.0"/>
<l c="ana" n="Araona" lng="-67.75" lat="-12.3333333333"/>
<l c="arp" n="Arapesh (Mountain)" lng="143.166666667" lat="-3.46666666667"/>
<l c="arc" n="Archi" lng="46.8333333333" lat="42.0"/>
<l c="arm" n="Armenian (Eastern)" lng="45.0" lat="40.0"/>
<l c="asm" n="Asmat" lng="138.5" lat="-5.5"/>
<l c="ata" n="Atayal" lng="121.333333333" lat="24.5"/>
<l c="ava" n="Avar" lng="46.5" lat="42.5"/>
<l c="awp" n="Awa Pit" lng="-78.25" lat="1.5"/>
<l c="awn" n="Awngi" lng="36.6666666667" lat="10.8333333333"/>
<l c="aym" n="Aymara (Central)" lng="-69.0" lat="-17.0"/>
<l c="aze" n="Azerbaijani" lng="48.5" lat="40.5"/>
<l c="bag" n="Bagirmi" lng="16.0" lat="11.6666666667"/>
<l c="bai" n="Bai" lng="100.0" lat="26.0"/>
<l c="baj" n="Bajau (Sama)" lng="123.0" lat="-4.33333333333"/>
<l c="bki" n="Bakairí" lng="-55.0" lat="-14.0"/>
<l c="bam" n="Bambara" lng="-7.5" lat="12.5"/>
<l c="brb" n="Bariba" lng="2.5" lat="10.0"/>
<l c="bsk" n="Bashkir" lng="58.0" lat="53.0"/>
<l c="bsq" n="Basque" lng="-3.0" lat="43.0"/>
<l c="bkr" n="Batak (Karo)" lng="98.25" lat="3.25"/>
<l c="bto" n="Batak (Toba)" lng="99.0" lat="2.5"/>
<l c="baw" n="Bawm" lng="92.25" lat="22.5"/>
<l c="bee" n="Beembe" lng="14.0833333333" lat="-3.91666666667"/>
<l c="bej" n="Beja" lng="36.0" lat="18.0"/>
<l c="bco" n="Bella Coola" lng="-126.666666667" lat="52.5"/>
<l c="ben" n="Bengali" lng="90.0" lat="24.0"/>
<l c="bma" n="Berber (Middle Atlas)" lng="-5.0" lat="33.0"/>
<l c="ber" n="Berta" lng="34.6666666667" lat="10.3333333333"/>
<l c="bir" n="Birom" lng="8.83333333333" lat="9.66666666667"/>
<l c="bis" n="Bisa" lng="-0.5" lat="11.5"/>
<l c="bbf" n="Bobo Madaré (Northern)" lng="-4.3333333333333" lat="12.4166666666667"/>
<l c="bod" n="Bodo" lng="92.0" lat="26.8333333333"/>
<l c="brh" n="Brahui" lng="67.0" lat="28.5"/>
<l c="bra" n="Brao" lng="107.5" lat="14.1666666667"/>
<l c="bre" n="Breton" lng="-3.0" lat="48.0"/>
<l c="bri" n="Bribri" lng="-83.0" lat="9.41666666667"/>
<l c="brw" n="Bru (Western)" lng="104.75" lat="16.75"/>
<l c="bul" n="Bulgarian" lng="25.0" lat="42.5"/>
<l c="brm" n="Burmese" lng="96.0" lat="21.0"/>
<l c="bur" n="Burushaski" lng="74.5" lat="36.5"/>
<l c="bet" n="Bété" lng="-6.25" lat="6.25"/>
<l c="cad" n="Caddo" lng="-93.5" lat="33.3333333333"/>
<l c="cah" n="Cahuilla" lng="-116.25" lat="33.5"/>
<l c="cax" n="Campa (Axininca)" lng="-74.0" lat="-12.0"/>
<l c="cam" n="Camsá" lng="-77.0" lat="1.16666666667"/>
<l c="cnl" n="Canela" lng="-45.0" lat="-7.0"/>
<l c="cnt" n="Cantonese" lng="113.0" lat="23.0"/>
<l c="car" n="Carib" lng="-56.0" lat="5.5"/>
<l c="ctl" n="Catalan" lng="2.0" lat="41.75"/>
<l c="cay" n="Cayapa" lng="-79.0" lat="0.666666666667"/>
<l c="cyv" n="Cayuvava" lng="-65.5" lat="-13.5"/>
<l c="chw" n="Cham (Western)" lng="105.5" lat="12.0"/>
<l c="cha" n="Chamorro" lng="144.75" lat="13.45"/>
<l c="cso" n="Chatino (Sierra Occidental)" lng="-97.3333333333" lat="16.25"/>
<l c="chl" n="Chehalis (Upper)" lng="-123.0" lat="46.5833333333"/>
<l c="che" n="Cherokee" lng="-83.5" lat="35.5"/>
<l c="cck" n="Chickasaw" lng="-88.0" lat="34.0"/>
<l c="cti" n="Chin (Tiddim)" lng="93.6666666667" lat="23.3333333333"/>
<l c="cle" n="Chinantec (Lealao)" lng="-95.9166666667" lat="17.3333333333"/>
<l c="chq" n="Chinantec (Quiotepec)" lng="-96.6666666667" lat="17.5833333333"/>
<l c="cve" n="Chuave" lng="145.116666667" lat="-6.11666666667"/>
<l c="chk" n="Chukchi" lng="-173.0" lat="67.0"/>
<l c="chv" n="Chuvash" lng="47.5" lat="55.5"/>
<l c="cil" n="CiLuba" lng="22.0" lat="-6.0"/>
<l c="ccp" n="Cocopa" lng="-115.0" lat="32.3333333333"/>
<l c="cof" n="Cofán" lng="-77.1666666667" lat="0.166666666667"/>
<l c="cmn" n="Comanche" lng="-101.5" lat="33.5"/>
<l c="coo" n="Coos (Hanis)" lng="-124.166666667" lat="43.5"/>
<l c="cre" n="Cree (Plains)" lng="-110.0" lat="54.0"/>
<l c="dad" n="Dadibi" lng="144.583333333" lat="-6.55"/>
<l c="dag" n="Daga" lng="149.333333333" lat="-10.0"/>
<l c="dgb" n="Dagbani" lng="-0.5" lat="9.58333333333"/>
<l c="dgr" n="Dagur" lng="124.0" lat="48.0"/>
<l c="dah" n="Dahalo" lng="40.5" lat="-2.33333333333"/>
<l c="ddf" n="Daju (Dar Fur)" lng="25.25" lat="12.25"/>
<l c="dan" n="Dan" lng="-8.0" lat="7.5"/>
<l c="dnw" n="Dangaléat (Western)" lng="18.3333333333" lat="12.1666666667"/>
<l c="dni" n="Dani (Lower Grand Valley)" lng="138.833333333" lat="-4.33333333333"/>
<l c="dar" n="Darai" lng="84.0" lat="24.0"/>
<l c="det" n="Deti" lng="24.5" lat="-20.5"/>
<l c="die" n="Diegueño (Mesa Grande)" lng="-116.166666667" lat="32.6666666667"/>
<l c="dio" n="Diola-Fogny" lng="-16.25" lat="13.0"/>
<l c="diz" n="Dizi" lng="36.5" lat="6.16666666667"/>
<l c="don" n="Dong (Southern)" lng="109.0" lat="27.0"/>
<l c="doy" n="Doyayo" lng="13.0833333333" lat="8.66666666667"/>
<l c="dre" n="Drehu" lng="167.25" lat="-21.0"/>
<l c="dum" n="Dumo" lng="141.3" lat="-2.68333333333"/>
<l c="efi" n="Efik" lng="8.5" lat="4.91666666667"/>
<l c="eja" n="Ejagham" lng="8.66666666667" lat="5.41666666667"/>
<l c="eng" n="English" lng="0.0" lat="52.0"/>
<l c="evn" n="Even" lng="130.0" lat="68.0"/>
<l c="eve" n="Evenki" lng="125.0" lat="56.0"/>
<l c="ewe" n="Ewe" lng="0.416666666667" lat="6.33333333333"/>
<l c="ewo" n="Ewondo" lng="12.0" lat="4.0"/>
<l c="fas" n="Fasu" lng="143.333333333" lat="-6.58333333333"/>
<l c="fef" n="Fe&#39;fe&#39;" lng="10.1666666667" lat="5.25"/>
<l c="fij" n="Fijian" lng="178.0" lat="-17.8333333333"/>
<l c="fin" n="Finnish" lng="25.0" lat="62.0"/>
<l c="fre" n="French" lng="2.0" lat="48.0"/>
<l c="ful" n="Fulniô" lng="-37.5" lat="-8.0"/>
<l c="fur" n="Fur" lng="25.0" lat="13.5"/>
<l c="fuz" n="Fuzhou" lng="119.5" lat="26.0"/>
<l c="fye" n="Fyem" lng="9.33333333333" lat="9.58333333333"/>
<l c="gar" n="Garo" lng="90.5" lat="25.6666666667"/>
<l c="gbb" n="Gbeya Bossangoa" lng="17.5" lat="6.66666666667"/>
<l c="gla" n="Gelao" lng="105.5" lat="22.9166666667"/>
<l c="geo" n="Georgian" lng="44.0" lat="42.0"/>
<l c="ger" n="German" lng="10.0" lat="52.0"/>
<l c="goa" n="Goajiro" lng="-72.0" lat="12.0"/>
<l c="grb" n="Grebo" lng="-8.0" lat="5.0"/>
<l c="grk" n="Greek (Modern)" lng="22.0" lat="39.0"/>
<l c="grw" n="Greenlandic (West)" lng="-51.0" lat="64.0"/>
<l c="ghb" n="Guahibo" lng="-69.0" lat="5.0"/>
<l c="gmb" n="Guambiano" lng="-76.6666666667" lat="2.5"/>
<l c="gua" n="Guaraní" lng="-56.0" lat="-26.0"/>
<l c="gwa" n="Gwari" lng="7.0" lat="9.5"/>
<l c="ga" n="Gã" lng="-0.166666666667" lat="5.66666666667"/>
<l c="had" n="Hadza" lng="35.1666666667" lat="-3.75"/>
<l c="hai" n="Haida" lng="-132.0" lat="53.0"/>
<l c="hak" n="Hakka" lng="116.0" lat="25.0"/>
<l c="hmr" n="Hamer" lng="36.5" lat="5.0"/>
<l c="ham" n="Hamtai" lng="146.25" lat="-7.5"/>
<l c="hau" n="Hausa" lng="7.0" lat="12.0"/>
<l c="hba" n="Hebrew (Modern Ashkenazic)" lng="35.1666666667" lat="31.75"/>
<l c="hin" n="Hindi" lng="77.0" lat="25.0"/>
<l c="hix" n="Hixkaryana" lng="-59.0" lat="-1.0"/>
<l c="hmo" n="Hmong Njua" lng="105.0" lat="28.0"/>
<l c="hop" n="Hopi" lng="-110.0" lat="36.0"/>
<l c="htc" n="Huastec" lng="-99.3333333333" lat="22.0833333333"/>
<l c="hve" n="Huave (San Mateo del Mar)" lng="-95.0" lat="16.2166666667"/>
<l c="hum" n="Huitoto (Murui)" lng="-73.5" lat="-1.0"/>
<l c="hun" n="Hungarian" lng="20.0" lat="47.0"/>
<l c="hzb" n="Hunzib" lng="46.25" lat="42.1666666667"/>
<l c="hup" n="Hupa" lng="-123.666666667" lat="41.0833333333"/>
<l c="iaa" n="Iaai" lng="166.583333333" lat="-20.4166666667"/>
<l c="iba" n="Iban" lng="112.0" lat="2.0"/>
<l c="igb" n="Igbo" lng="7.33333333333" lat="6.0"/>
<l c="ign" n="Ignaciano" lng="-65.4166666667" lat="-15.1666666667"/>
<l c="ijo" n="Ijo (Kolokuma)" lng="5.66666666667" lat="4.91666666667"/>
<l c="ik" n="Ik" lng="34.1666666667" lat="3.75"/>
<l c="ika" n="Ika" lng="-73.75" lat="10.6666666667"/>
<l c="imo" n="Imonda" lng="141.166666667" lat="-3.33333333333"/>
<l c="ind" n="Indonesian" lng="106.0" lat="0.0"/>
<l c="igs" n="Ingessana" lng="34.0" lat="11.5"/>
<l c="ing" n="Ingush" lng="45.0833333333" lat="43.1666666667"/>
<l c="irx" n="Iranxe" lng="-58.0" lat="-13.0"/>
<l c="irq" n="Iraqw" lng="35.5" lat="-4.0"/>
<l c="irr" n="Irarutu" lng="133.5" lat="-3.0"/>
<l c="ird" n="Irish (Donegal)" lng="-8.0" lat="55.0"/>
<l c="iso" n="Isoko" lng="6.25" lat="5.5"/>
<l c="ite" n="Itelmen" lng="157.5" lat="57.0"/>
<l c="ito" n="Itonama" lng="-64.3333333333" lat="-12.8333333333"/>
<l c="iva" n="Ivatan" lng="122.0" lat="20.5"/>
<l c="iwm" n="Iwam" lng="142.0" lat="-4.33333333333"/>
<l c="jak" n="Jakaltek" lng="-91.6666666667" lat="15.6666666667"/>
<l c="jpn" n="Japanese" lng="140.0" lat="37.0"/>
<l c="jpr" n="Japreria" lng="-73.0" lat="10.5"/>
<l c="jaq" n="Jaqaru" lng="-76.0" lat="-13.0"/>
<l c="jav" n="Javanese" lng="111.0" lat="-7.0"/>
<l c="jeb" n="Jebero" lng="-76.5" lat="-5.41666666667"/>
<l c="jeh" n="Jeh" lng="107.833333333" lat="15.1666666667"/>
<l c="jng" n="Jingpho" lng="97.0" lat="25.4166666667"/>
<l c="jiv" n="Jivaro" lng="-78.0" lat="-2.5"/>
<l c="jom" n="Jomang" lng="30.5" lat="10.5833333333"/>
<l c="juh" n="Ju|&#39;hoan" lng="21.0" lat="-19.0"/>
<l c="kek" n="K&#39;ekchí" lng="-89.8333333333" lat="16.0"/>
<l c="kab" n="Kabardian" lng="43.5" lat="43.5"/>
<l c="kad" n="Kadugli" lng="29.6666666667" lat="11.0"/>
<l c="kly" n="Kala Lagaw Ya" lng="142.116666667" lat="-10.1166666667"/>
<l c="kal" n="Kalami" lng="72.5" lat="35.5"/>
<l c="knk" n="Kanakuru" lng="12.0" lat="10.0"/>
<l c="knd" n="Kannada" lng="76.0" lat="14.0"/>
<l c="knr" n="Kanuri" lng="13.0" lat="12.0"/>
<l c="ksg" n="Karen (Sgaw)" lng="97.0" lat="18.0"/>
<l c="krk" n="Karok" lng="-123.0" lat="41.6666666667"/>
<l c="kas" n="Kashmiri" lng="76.0" lat="34.0"/>
<l c="kws" n="Kawaiisu" lng="-117.5" lat="36.0"/>
<l c="kyl" n="Kayah Li (Eastern)" lng="97.5" lat="19.0"/>
<l c="ked" n="Kedang" lng="123.75" lat="-8.25"/>
<l c="kef" n="Kefa" lng="36.25" lat="7.25"/>
<l c="ker" n="Kera" lng="15.0833333333" lat="9.83333333333"/>
<l c="ket" n="Ket" lng="87.0" lat="64.0"/>
<l c="kew" n="Kewa" lng="143.833333333" lat="-6.5"/>
<l c="kha" n="Khalkha" lng="105.0" lat="47.0"/>
<l c="kty" n="Khanty" lng="65.0" lat="65.0"/>
<l c="khr" n="Kharia" lng="84.3333333333" lat="22.5"/>
<l c="khs" n="Khasi" lng="92.0" lat="25.5"/>
<l c="khm" n="Khmer" lng="105.0" lat="12.5"/>
<l c="kmu" n="Khmu&#39;" lng="102.0" lat="21.0"/>
<l c="klv" n="Kilivila" lng="151.083333333" lat="-8.5"/>
<l c="kio" n="Kiowa" lng="-99.0" lat="37.0"/>
<l c="kgz" n="Kirghiz" lng="75.0" lat="42.0"/>
<l c="kss" n="Kisi (Southern)" lng="-10.25" lat="8.5"/>
<l c="kiw" n="Kiwai (Southern)" lng="143.5" lat="-8.0"/>
<l c="klm" n="Klamath" lng="-121.5" lat="42.5"/>
<l c="koa" n="Koasati" lng="-85.1666666667" lat="34.8333333333"/>
<l c="kob" n="Kobon" lng="144.333333333" lat="-5.16666666667"/>
<l c="koh" n="Kohumono" lng="8.11666666667" lat="6.0"/>
<l c="koi" n="Koiari" lng="147.333333333" lat="-9.5"/>
<l c="kzy" n="Komi-Zyrian" lng="55.0" lat="65.0"/>
<l c="kom" n="Komo" lng="33.75" lat="8.75"/>
<l c="kkn" n="Konkani" lng="74.0" lat="15.25"/>
<l c="kgi" n="Konyagi" lng="-13.25" lat="12.5"/>
<l c="kor" n="Korean" lng="128.0" lat="37.5"/>
<l c="kfe" n="Koromfe" lng="-0.916666666667" lat="14.25"/>
<l c="kry" n="Koryak" lng="167.0" lat="61.0"/>
<l c="kot" n="Kota" lng="77.1666666667" lat="11.5"/>
<l c="ktk" n="Kotoko" lng="15.3333333333" lat="11.3333333333"/>
<l c="koy" n="Koya" lng="81.3333333333" lat="17.5"/>
<l c="kch" n="Koyra Chiini" lng="-3.0" lat="17.0"/>
<l c="kse" n="Koyraboro Senni" lng="0.0" lat="16.0"/>
<l c="kpe" n="Kpelle" lng="-10.0" lat="7.0"/>
<l c="kro" n="Krongo" lng="30.0" lat="10.5"/>
<l c="kul" n="Kullo" lng="37.0833333333" lat="6.75"/>
<l c="kun" n="Kuna" lng="-77.3333333333" lat="8.0"/>
<l c="knm" n="Kunama" lng="37.0" lat="14.5"/>
<l c="kmp" n="Kunimaipa" lng="146.833333333" lat="-8.0"/>
<l c="krd" n="Kurdish (Central)" lng="44.0" lat="36.0"/>
<l c="kur" n="Kurukh" lng="85.5" lat="22.8333333333"/>
<l c="kut" n="Kutenai" lng="-116.0" lat="49.5"/>
<l c="kwa" n="Kwaio" lng="161.0" lat="-8.95"/>
<l c="kwk" n="Kwakw&#39;ala" lng="-127.0" lat="51.0"/>
<l c="kwo" n="Kwoma" lng="142.75" lat="-4.16666666667"/>
<l c="lad" n="Ladakhi" lng="78.0" lat="34.0"/>
<l c="lah" n="Lahu" lng="98.1666666667" lat="20.0"/>
<l c="lak" n="Lak" lng="47.1666666667" lat="42.1666666667"/>
<l c="lkt" n="Lakhota" lng="-101.833333333" lat="43.8333333333"/>
<l c="lkk" n="Lakkia" lng="110.166666667" lat="24.0833333333"/>
<l c="lam" n="Lamé" lng="14.5" lat="9.0"/>
<l c="lat" n="Latvian" lng="24.0" lat="57.0"/>
<l c="lav" n="Lavukaleve" lng="159.2" lat="-9.08333333333"/>
<l c="llm" n="Lelemi" lng="0.5" lat="7.33333333333"/>
<l c="len" n="Lenakel" lng="169.25" lat="-19.45"/>
<l c="lep" n="Lepcha" lng="88.5" lat="27.1666666667"/>
<l c="lez" n="Lezgian" lng="47.8333333333" lat="41.6666666667"/>
<l c="lit" n="Lithuanian" lng="24.0" lat="55.0"/>
<l c="lua" n="Lua" lng="17.75" lat="9.75"/>
<l c="lug" n="Lugbara" lng="30.9166666667" lat="3.08333333333"/>
<l c="lui" n="Luiseño" lng="-117.166666667" lat="33.3333333333"/>
<l c="luo" n="Luo" lng="34.75" lat="-0.5"/>
<l c="lus" n="Lushootseed" lng="-122.0" lat="48.0"/>
<l c="kkv" n="Lusi" lng="149.666666667" lat="-5.58333333333"/>
<l c="luv" n="Luvale" lng="22.0" lat="-12.0"/>
<l c="lu" n="Lü" lng="100.666666667" lat="22.0"/>
<l c="mya" n="Ma&#39;ya" lng="130.916666667" lat="-1.25"/>
<l c="maa" n="Maasai" lng="36.0" lat="-3.0"/>
<l c="mab" n="Maba" lng="20.8333333333" lat="13.75"/>
<l c="mne" n="Maidu (Northeast)" lng="-120.666666667" lat="40.0"/>
<l c="mak" n="Makah" lng="-124.666666667" lat="48.3333333333"/>
<l c="mal" n="Malagasy" lng="47.0" lat="-20.0"/>
<l c="mla" n="Mambila" lng="11.5" lat="6.75"/>
<l c="mnc" n="Manchu" lng="127.5" lat="49.5"/>
<l c="mnd" n="Mandarin" lng="110.0" lat="34.0"/>
<l c="mgg" n="Mangghuer" lng="102.0" lat="36.0"/>
<l c="mao" n="Maori" lng="176.0" lat="-40.0"/>
<l c="map" n="Mapudungun" lng="-72.0" lat="-38.0"/>
<l c="mrg" n="Margi" lng="13.0" lat="11.0"/>
<l c="mme" n="Mari (Meadow)" lng="48.0" lat="57.0"/>
<l c="mar" n="Maricopa" lng="-113.166666667" lat="33.1666666667"/>
<l c="mrd" n="Marind" lng="140.166666667" lat="-7.83333333333"/>
<l c="mau" n="Maung" lng="133.5" lat="-11.9166666667"/>
<l c="may" n="Maybrat" lng="132.5" lat="-1.33333333333"/>
<l c="maz" n="Mazahua" lng="-99.9166666667" lat="19.4166666667"/>
<l c="mzc" n="Mazatec (Chiquihuitlán)" lng="-96.9166666667" lat="17.75"/>
<l c="mba" n="Mba" lng="25.0" lat="1.0"/>
<l c="mbm" n="Mbum" lng="13.1666666667" lat="7.75"/>
<l c="mei" n="Meithei" lng="94.0" lat="24.75"/>
<l c="mie" n="Mien" lng="111.0" lat="25.0"/>
<l c="hok" n="Min (Southern)" lng="118.0" lat="25.0"/>
<l c="mss" n="Miwok (Southern Sierra)" lng="-120.0" lat="37.5"/>
<l c="mtp" n="Mixe (Totontepec)" lng="-96.0" lat="17.25"/>
<l c="mxc" n="Mixtec (Chalcatongo)" lng="-97.5833333333" lat="17.05"/>
<l c="mxm" n="Mixtec (Molinos)" lng="-97.5833333333" lat="17.0"/>
<l c="mog" n="Moghol" lng="62.0" lat="35.0"/>
<l c="mor" n="Mor" lng="135.75" lat="-2.95"/>
<l c="mro" n="Moro" lng="30.1666666667" lat="11.0"/>
<l c="mov" n="Movima" lng="-65.6666666667" lat="-13.8333333333"/>
<l c="mui" n="Muinane" lng="-72.5" lat="-1.0"/>
<l c="mum" n="Mumuye" lng="11.6666666667" lat="9.0"/>
<l c="mun" n="Mundari" lng="84.6666666667" lat="23.0"/>
<l c="mrl" n="Murle" lng="33.5" lat="6.5"/>
<l c="nhn" n="Nahuatl (North Puebla)" lng="-98.25" lat="20.0"/>
<l c="nht" n="Nahuatl (Tetelcingo)" lng="-99.0" lat="19.6666666667"/>
<l c="kho" n="Nama" lng="18.0" lat="-25.5"/>
<l c="nmb" n="Nambikuára (Southern)" lng="-59.5" lat="-14.0"/>
<l c="nai" n="Nanai" lng="137.0" lat="49.5"/>
<l c="nnc" n="Nancowry" lng="93.5" lat="8.05"/>
<l c="nan" n="Nandi" lng="35.0" lat="0.25"/>
<l c="nar" n="Nara (in Ethiopia)" lng="37.5833333333" lat="15.0833333333"/>
<l c="nas" n="Nasioi" lng="155.583333333" lat="-6.33333333333"/>
<l c="nbk" n="Natügu" lng="165.866666667" lat="-10.7833333333"/>
<l c="nav" n="Navajo" lng="-108.0" lat="36.1666666667"/>
<l c="nax" n="Naxi" lng="100.0" lat="27.5"/>
<l c="ndt" n="Ndut" lng="-16.9166666667" lat="14.9166666667"/>
<l c="ndy" n="Ndyuka" lng="-54.5" lat="4.5"/>
<l c="ntu" n="Nenets" lng="76.0" lat="70.0"/>
<l c="nap" n="Neo-Aramaic (Persian Azerbaijan)" lng="47.0" lat="38.0"/>
<l c="nep" n="Nepali" lng="85.0" lat="28.0"/>
<l c="new" n="Newari (Kathmandu)" lng="85.5" lat="27.6666666667"/>
<l c="nez" n="Nez Perce" lng="-116.0" lat="46.0"/>
<l c="nga" n="Nganasan" lng="93.0" lat="71.0"/>
<l c="nti" n="Ngiti" lng="30.25" lat="1.33333333333"/>
<l c="ngi" n="Ngiyambaa" lng="145.5" lat="-31.75"/>
<l c="ngz" n="Ngizim" lng="10.9166666667" lat="12.0833333333"/>
<l c="nim" n="Nimboran" lng="140.166666667" lat="-2.5"/>
<l c="chu" n="Nivacle" lng="-60.5" lat="-23.5"/>
<l c="niv" n="Nivkh" lng="142.0" lat="53.3333333333"/>
<l c="nko" n="Nkore-Kiga" lng="29.8333333333" lat="-0.916666666667"/>
<l c="nob" n="Nobiin" lng="31.0" lat="21.0"/>
<l c="non" n="Noni" lng="10.5833333333" lat="6.41666666667"/>
<l c="nor" n="Norwegian" lng="8.0" lat="61.0"/>
<l c="nun" n="Nung (in Vietnam)" lng="106.416666667" lat="21.9166666667"/>
<l c="nuu" n="Nuuchahnulth" lng="-126.666666667" lat="49.6666666667"/>
<l c="nkt" n="Nyah Kur (Tha Pong)" lng="101.666666667" lat="15.6666666667"/>
<l c="nyg" n="Nyangi" lng="33.5833333333" lat="3.41666666667"/>
<l c="nyi" n="Nyimang" lng="29.3333333333" lat="12.1666666667"/>
<l c="nis" n="Nyishi" lng="93.5" lat="27.5"/>
<l c="ood" n="O&#39;odham" lng="-112.0" lat="32.0"/>
<l c="oca" n="Ocaina" lng="-71.75" lat="-2.75"/>
<l c="ogb" n="Ogbia" lng="6.25" lat="4.66666666667"/>
<l c="oji" n="Ojibwa (Eastern)" lng="-80.0" lat="46.0"/>
<l c="orm" n="Ormuri" lng="69.75" lat="32.5"/>
<l c="orh" n="Oromo (Harar)" lng="42.0" lat="9.0"/>
<l c="otm" n="Otomí (Mezquital)" lng="-99.1666666667" lat="20.1666666667"/>
<l c="pms" n="Paamese" lng="168.25" lat="-16.5"/>
<l c="pac" n="Pacoh" lng="107.083333333" lat="16.4166666667"/>
<l c="pai" n="Paiwan" lng="120.833333333" lat="22.5"/>
<l c="puk" n="Parauk" lng="99.5" lat="23.25"/>
<l c="psh" n="Pashto" lng="67.0" lat="33.0"/>
<l c="psm" n="Passamaquoddy-Maliseet" lng="-67.0" lat="45.0"/>
<l c="pau" n="Paumarí" lng="-64.0" lat="-6.0"/>
<l c="paw" n="Pawaian" lng="145.083333333" lat="-7.0"/>
<l c="pec" n="Pech" lng="-85.5" lat="15.0"/>
<l c="prs" n="Persian" lng="54.0" lat="32.0"/>
<l c="phl" n="Phlong" lng="99.0" lat="15.0"/>
<l c="poa" n="Po-Ai" lng="164.833333333" lat="-20.6666666667"/>
<l c="poh" n="Pohnpeian" lng="158.25" lat="6.88333333333"/>
<l c="pol" n="Polish" lng="20.0" lat="52.0"/>
<l c="pso" n="Pomo (Southeastern)" lng="-122.5" lat="39.0"/>
<l c="pur" n="Purépecha" lng="-101.666666667" lat="19.5"/>
<l c="pae" n="Páez" lng="-76.0" lat="2.66666666667"/>
<l c="bng" n="Qaqet" lng="152.0" lat="-4.58333333333"/>
<l c="qaw" n="Qawasqar" lng="-75.0" lat="-49.0"/>
<l c="qco" n="Quechua (Cochabamba)" lng="-66.0" lat="-17.5"/>
<l c="ram" n="Rama" lng="-83.75" lat="11.75"/>
<l c="rap" n="Rapanui" lng="-109.366666667" lat="-27.1166666667"/>
<l c="res" n="Resígaro" lng="-71.5" lat="-2.41666666667"/>
<l c="rom" n="Romanian" lng="25.0" lat="46.0"/>
<l c="rsc" n="Romansch (Scharans)" lng="9.5" lat="46.75"/>
<l c="ror" n="Roro" lng="146.583333333" lat="-8.75"/>
<l c="ruk" n="Rukai (Tanan)" lng="120.833333333" lat="22.8333333333"/>
<l c="rus" n="Russian" lng="38.0" lat="56.0"/>
<l c="rut" n="Rutul" lng="47.4166666667" lat="41.5"/>
<l c="sab" n="Sa&#39;ban" lng="115.666666667" lat="3.66666666667"/>
<l c="scs" n="Saami (Central-South)" lng="16.75" lat="64.6666666667"/>
<l c="sdw" n="Sandawe" lng="35.0" lat="-5.0"/>
<l c="san" n="Sango" lng="18.0" lat="5.0"/>
<l c="snm" n="Sanuma" lng="-64.6666666667" lat="4.5"/>
<l c="svs" n="Savosavo" lng="159.8" lat="-9.13333333333"/>
<l c="seb" n="Sebei" lng="34.5833333333" lat="1.33333333333"/>
<l c="sed" n="Sedang" lng="108.0" lat="14.8333333333"/>
<l c="slp" n="Selepet" lng="147.166666667" lat="-6.16666666667"/>
<l c="sel" n="Selknam" lng="-70.0" lat="-53.0"/>
<l c="skp" n="Selkup" lng="82.0" lat="65.0"/>
<l c="sml" n="Semelai" lng="103.0" lat="3.0"/>
<l c="snd" n="Senadi" lng="-6.25" lat="9.5"/>
<l c="snc" n="Seneca" lng="-77.5" lat="42.5"/>
<l c="snt" n="Sentani" lng="140.583333333" lat="-2.58333333333"/>
<l c="sha" n="Shan" lng="98.0" lat="22.0"/>
<l c="shs" n="Shasta" lng="-122.666666667" lat="41.8333333333"/>
<l c="shk" n="Shipibo-Konibo" lng="-75.0" lat="-7.5"/>
<l c="shi" n="Shiriana" lng="-62.8333333333" lat="3.5"/>
<l c="shu" n="Shuswap" lng="-120.0" lat="52.0"/>
<l c="sdh" n="Sindhi" lng="69.0" lat="26.0"/>
<l c="snh" n="Sinhala" lng="80.5" lat="7.0"/>
<l c="sin" n="Siona" lng="-76.25" lat="0.333333333333"/>
<l c="srn" n="Sirionó" lng="-64.0" lat="-15.5833333333"/>
<l c="sla" n="Slave" lng="-125.0" lat="67.0"/>
<l c="som" n="Somali" lng="45.0" lat="3.0"/>
<l c="soq" n="Soqotri" lng="54.0" lat="12.5"/>
<l c="sor" n="Sora" lng="84.3333333333" lat="20.0"/>
<l c="spa" n="Spanish" lng="-4.0" lat="40.0"/>
<l c="squ" n="Squamish" lng="-123.166666667" lat="49.6666666667"/>
<l c="sre" n="Sre" lng="108.0" lat="11.5"/>
<l c="sue" n="Suena" lng="147.55" lat="-7.75"/>
<l c="sui" n="Sui" lng="107.5" lat="26.0"/>
<l c="sup" n="Supyire" lng="-5.58333333333" lat="11.5"/>
<l c="swa" n="Swahili" lng="39.0" lat="-6.5"/>
<l c="sba" n="Sáliba (in Colombia)" lng="-70.0" lat="6.0"/>
<l c="tab" n="Taba" lng="127.5" lat="0.0"/>
<l c="tac" n="Tacana" lng="-68.0" lat="-13.5"/>
<l c="tag" n="Tagalog" lng="121.0" lat="15.0"/>
<l c="tma" n="Tama" lng="22.0" lat="14.5"/>
<l c="tam" n="Tamang (Eastern)" lng="85.666666666667" lat="27.5"/>
<l c="tmp" n="Tampulma" lng="-0.583333333333" lat="10.4166666667"/>
<l c="tok" n="Tarok" lng="10.0833333333" lat="9.0"/>
<l c="tas" n="Tashlhiyt" lng="-5.0" lat="31.0"/>
<l c="tsg" n="Tausug" lng="121.0" lat="6.0"/>
<l c="teh" n="Tehuelche" lng="-68.0" lat="-48.0"/>
<l c="tks" n="Teke (Southern)" lng="14.5" lat="-2.33333333333"/>
<l c="tel" n="Telugu" lng="79.0" lat="16.0"/>
<l c="tmn" n="Temein" lng="29.4166666667" lat="11.9166666667"/>
<l c="tne" n="Temne" lng="-13.0833333333" lat="8.66666666667"/>
<l c="ter" n="Tera" lng="11.8333333333" lat="11.0"/>
<l c="ttn" n="Tetun" lng="126.0" lat="-9.0"/>
<l c="tha" n="Thai" lng="101.0" lat="16.0"/>
<l c="tib" n="Tibetan (Standard Spoken)" lng="91.0" lat="30.0"/>
<l c="tic" n="Ticuna" lng="-70.5" lat="-4.0"/>
<l c="tgk" n="Tigak" lng="150.8" lat="-2.71666666667"/>
<l c="tgr" n="Tigré" lng="38.5" lat="16.5"/>
<l c="try" n="Tiruray" lng="124.166666667" lat="6.75"/>
<l c="twn" n="Tiwa (Northern)" lng="-105.5" lat="36.5"/>
<l c="tiw" n="Tiwi" lng="131.0" lat="-11.5"/>
<l c="tlp" n="Tlapanec" lng="-99.0" lat="17.0833333333"/>
<l c="toa" n="Toaripi" lng="146.25" lat="-8.33333333333"/>
<l c="tol" n="Tol" lng="-87.0" lat="14.6666666667"/>
<l c="ton" n="Tonkawa" lng="-96.75" lat="30.25"/>
<l c="dts" n="Toro So" lng="-3.25" lat="14.4166666667"/>
<l c="tpa" n="Totonac (Papantla)" lng="-97.3333333333" lat="20.3333333333"/>
<l c="tru" n="Trumai" lng="-53.5833333333" lat="-11.9166666667"/>
<l c="tsi" n="Tsimshian (Coast)" lng="-129.0" lat="52.5"/>
<l c="tso" n="Tsou" lng="120.75" lat="23.5"/>
<l c="ttu" n="Tsova-Tush" lng="45.5" lat="42.5"/>
<l c="tug" n="Tuareg (Ahaggar)" lng="6.0" lat="23.0"/>
<l c="tuk" n="Tukang Besi" lng="123.5" lat="-5.5"/>
<l c="tul" n="Tulu" lng="75.3333333333" lat="12.75"/>
<l c="tun" n="Tunica" lng="-91.0" lat="32.6666666667"/>
<l c="tur" n="Turkish" lng="35.0" lat="39.0"/>
<l c="tuv" n="Tuvan" lng="95.0" lat="52.0"/>
<l c="tza" n="Tzeltal (Aguacatenango)" lng="-92.5" lat="16.4166666667"/>
<l c="umb" n="UMbundu" lng="15.0" lat="-12.5"/>
<l c="una" n="Una" lng="140.0" lat="-4.66666666667"/>
<l c="urk" n="Urubú-Kaapor" lng="-46.5" lat="-2.33333333333"/>
<l c="usa" n="Usan" lng="145.166666667" lat="-4.83333333333"/>
<l c="uzn" n="Uzbek (Northern)" lng="66.5" lat="40.6666666667"/>
<l c="vie" n="Vietnamese" lng="106.5" lat="10.5"/>
<l c="wnt" n="Wantoat" lng="146.5" lat="-6.16666666667"/>
<l c="wps" n="Wapishana" lng="-60.0" lat="2.66666666667"/>
<l c="wap" n="Wappo" lng="-122.5" lat="38.5"/>
<l c="wra" n="Warao" lng="-61.6666666667" lat="9.33333333333"/>
<l c="wrs" n="Waris" lng="141.0" lat="-3.16666666667"/>
<l c="wma" n="West Makian" lng="127.583333333" lat="0.5"/>
<l c="wch" n="Wichí" lng="-62.5833333333" lat="-22.5"/>
<l c="win" n="Wintu" lng="-122.5" lat="41.0"/>
<l c="wiy" n="Wiyot" lng="-124.166666667" lat="40.8333333333"/>
<l c="woi" n="Woisika" lng="124.833333333" lat="-8.25"/>
<l c="wlf" n="Wolof" lng="-16.0" lat="15.25"/>
<l c="wuc" n="Wu" lng="119.916666667" lat="31.6666666667"/>
<l c="ygr" n="Yagaria" lng="145.416666667" lat="-6.33333333333"/>
<l c="ykt" n="Yakut" lng="130.0" lat="62.0"/>
<l c="yan" n="Yana" lng="-122.0" lat="40.5"/>
<l c="yap" n="Yapese" lng="138.166666667" lat="9.58333333333"/>
<l c="yaq" n="Yaqui" lng="-110.25" lat="27.5"/>
<l c="yar" n="Yareba" lng="148.5" lat="-9.5"/>
<l c="yaw" n="Yawa" lng="136.25" lat="-1.75"/>
<l c="yay" n="Yay" lng="104.75" lat="22.4166666667"/>
<l c="yes" n="Yessan-Mayo" lng="142.583333333" lat="-4.16666666667"/>
<l c="yey" n="Yeyi" lng="23.5" lat="-20.0"/>
<l c="yor" n="Yoruba" lng="4.33333333333" lat="8.0"/>
<l c="yct" n="Yucatec" lng="-89.0" lat="20.0"/>
<l c="yuc" n="Yuchi" lng="-86.75" lat="35.75"/>
<l c="ycn" n="Yucuna" lng="-71.0" lat="-0.75"/>
<l c="yko" n="Yukaghir (Kolyma)" lng="150.833333333" lat="65.75"/>
<l c="ytu" n="Yukaghir (Tundra)" lng="155.0" lat="69.0"/>
<l c="yul" n="Yulu" lng="25.25" lat="8.5"/>
<l c="yus" n="Yupik (Siberian)" lng="-173.0" lat="65.0"/>
<l c="yur" n="Yurok" lng="-124.0" lat="41.3333333333"/>
<l c="zan" n="Zande" lng="26.0" lat="4.0"/>
<l c="zqc" n="Zoque (Copainalá)" lng="-93.25" lat="17.0"/>
<l c="zul" n="Zulu" lng="30.0" lat="-30.0"/>
<l c="zun" n="Zuni" lng="-108.833333333" lat="35.0833333333"/>
</v>
<v numeric="2" description="No bilabials" icon_id="c0000dd" icon_url="https://wals.info/clld-static/icons/c0000dd.png" zindex="0">
<l c="chp" n="Chipewyan" lng="-106.0" lat="59.0"/>
<l c="ond" n="Oneida" lng="-75.6666666667" lat="43.0"/>
<l c="tli" n="Tlingit" lng="-135.0" lat="59.0"/>
<l c="wic" n="Wichita" lng="-97.3333333333" lat="33.3333333333"/>
</v>
<v numeric="3" description="No fricatives" icon_id="cffff00" icon_url="https://wals.info/clld-static/icons/cffff00.png" zindex="0">
<l c="alw" n="Alawa" lng="134.25" lat="-15.1666666667"/>
<l c="ant" n="Angaataha" lng="146.25" lat="-7.21666666667"/>
<l c="amp" n="Arrernte (Mparntwe)" lng="136.0" lat="-24.0"/>
<l c="byu" n="Bandjalang (Yugumbir)" lng="153.0" lat="-27.9166666667"/>
<l c="brd" n="Bardi" lng="122.916666667" lat="-16.5833333333"/>
<l c="brr" n="Bororo" lng="-57.0" lat="-16.0"/>
<l c="bua" n="Burarra" lng="134.583333333" lat="-12.25"/>
<l c="cac" n="Cacua" lng="-70.0" lat="1.08333333333"/>
<l c="din" n="Dinka" lng="28.0" lat="8.5"/>
<l c="diy" n="Diyari" lng="139.0" lat="-28.0"/>
<l c="djp" n="Djapu" lng="136.0" lat="-12.6666666667"/>
<l c="der" n="Dla (Proper)" lng="141.0" lat="-3.58333333333"/>
<l c="dyi" n="Dyirbal" lng="145.583333333" lat="-17.8333333333"/>
<l c="eka" n="Ekari" lng="135.5" lat="-3.83333333333"/>
<l c="gds" n="Gadsup" lng="146.0" lat="-6.25"/>
<l c="grr" n="Garrwa" lng="137.166666667" lat="-17.0833333333"/>
<l c="goo" n="Gooniyandi" lng="126.333333333" lat="-18.3333333333"/>
<l c="gan" n="Great Andamanese" lng="92.6666666667" lat="12.0"/>
<l c="haw" n="Hawaiian" lng="-155.5" lat="19.5833333333"/>
<l c="kgu" n="Kalkatungu" lng="139.5" lat="-21.0"/>
<l c="kay" n="Kayardild" lng="139.5" lat="-17.05"/>
<l c="krb" n="Kiribati" lng="173.0" lat="1.33333333333"/>
<l c="kya" n="Kuku-Yalanji" lng="145.0" lat="-16.0"/>
<l c="lan" n="Lango" lng="33.0" lat="2.16666666667"/>
<l c="mlk" n="Malakmalak" lng="130.416666667" lat="-13.4166666667"/>
<l c="myi" n="Mangarrayi" lng="133.5" lat="-14.6666666667"/>
<l c="mrn" n="Maranao" lng="124.25" lat="7.83333333333"/>
<l c="mku" n="Maranungku" lng="130.0" lat="-13.6666666667"/>
<l c="mrt" n="Martuthunira" lng="116.5" lat="-20.8333333333"/>
<l c="mbb" n="Mbabaram" lng="145.0" lat="-17.1666666667"/>
<l c="mpa" n="Murrinh-Patha" lng="129.666666667" lat="-14.6666666667"/>
<l c="nug" n="Nunggubuyu" lng="135.666666667" lat="-13.75"/>
<l c="pnr" n="Panare" lng="-66.0" lat="6.5"/>
<l c="pit" n="Pitjantjatjara" lng="130.0" lat="-26.0"/>
<l c="ung" n="Ungarinjin" lng="126.0" lat="-16.3333333333"/>
<l c="wah" n="Wahgi" lng="144.716666667" lat="-5.83333333333"/>
<l c="wam" n="Wambaya" lng="135.75" lat="-18.6666666667"/>
<l c="wao" n="Waorani" lng="-76.5" lat="-1.0"/>
<l c="wry" n="Waray (in Australia)" lng="131.25" lat="-13.1666666667"/>
<l c="wrd" n="Wardaman" lng="131.0" lat="-15.5"/>
<l c="war" n="Wari&#39;" lng="-65.0" lat="-11.3333333333"/>
<l c="wdo" n="Western Desert (Ooldea)" lng="132.0" lat="-30.5"/>
<l c="wmu" n="Wik Munkan" lng="141.75" lat="-13.9166666667"/>
<l c="yag" n="Yagua" lng="-72.0" lat="-3.5"/>
<l c="yny" n="Yanyuwa" lng="137.166666667" lat="-16.4166666667"/>
<l c="yel" n="Yelî Dnye" lng="154.166666667" lat="-11.3666666667"/>
<l c="yid" n="Yidiny" lng="145.75" lat="-17.0"/>
<l c="yim" n="Yimas" lng="143.55" lat="-4.66666666667"/>
</v>
<v numeric="4" description="No nasals" icon_id="cdd0000" icon_url="https://wals.info/clld-static/icons/cdd0000.png" zindex="0">
<l c="adk" n="Andoke" lng="-72.0" lat="-0.666666666667"/>
<l c="cub" n="Cubeo" lng="-70.5" lat="1.33333333333"/>
<l c="epe" n="Epena Pedee" lng="-77.0" lat="3.0"/>
<l c="kng" n="Kaingang" lng="-52.0" lat="-26.0"/>
<l c="kla" n="Klao" lng="-8.75" lat="4.75"/>
<l c="kpa" n="Kpan" lng="10.1666666667" lat="7.58333333333"/>
<l c="prh" n="Pirahã" lng="-62.0" lat="-7.0"/>
<l c="qui" n="Quileute" lng="-124.25" lat="47.9166666667"/>
<l c="rtk" n="Rotokas" lng="155.166666667" lat="-6.0"/>
<l c="bno" n="Waimaha" lng="-70.25" lat="0.333333333333"/>
</v>
<v numeric="5" description="No bilabials or nasals" icon_id="c990099" icon_url="https://wals.info/clld-static/icons/c990099.png" zindex="0">
<l c="eya" n="Eyak" lng="-145.0" lat="60.5"/>
</v>
<v numeric="6" description="No fricatives or nasals" icon_id="cff6600" icon_url="https://wals.info/clld-static/icons/cff6600.png" zindex="0">
<l c="max" n="Maxakalí" lng="-40.0" lat="-18.0"/>
</v>
</feature>
"""

WALS_131A_NUMERALS = """
<feature number="131A" base_url="https://wals.info/" name="Numeral Bases">
<description>
<url>https://wals.info/feature/131A.xml</url>
<timestamp>2024-10-18T11:59:12.029308+02:00</timestamp>
</description>
<v numeric="1" description="Decimal" icon_id="c0000dd" icon_url="https://wals.info/clld-static/icons/c0000dd.png" zindex="0">
<l c="abu" n="Abun" lng="132.5" lat="-0.5"/>
<l c="aco" n="Acoma" lng="-107.583333333" lat="34.9166666667"/>
<l c="abm" n="Alabama" lng="-87.4166666667" lat="32.3333333333"/>
<l c="alb" n="Albanian" lng="20.0" lat="41.0"/>
<l c="amh" n="Amharic" lng="38.0" lat="10.0"/>
<l c="aeg" n="Arabic (Egyptian)" lng="31.0" lat="30.0"/>
<l c="arc" n="Archi" lng="46.8333333333" lat="42.0"/>
<l c="arm" n="Armenian (Eastern)" lng="45.0" lat="40.0"/>
<l c="aym" n="Aymara (Central)" lng="-69.0" lat="-17.0"/>
<l c="bag" n="Bagirmi" lng="16.0" lat="11.6666666667"/>
<l c="bam" n="Bambara" lng="-7.5" lat="12.5"/>
<l c="bas" n="Basaá" lng="10.5" lat="3.91666666667"/>
<l c="bkr" n="Batak (Karo)" lng="98.25" lat="3.25"/>
<l c="baw" n="Bawm" lng="92.25" lat="22.5"/>
<l c="bma" n="Berber (Middle Atlas)" lng="-5.0" lat="33.0"/>
<l c="brh" n="Brahui" lng="67.0" lat="28.5"/>
<l c="bri" n="Bribri" lng="-83.0" lat="9.41666666667"/>
<l c="brm" n="Burmese" lng="96.0" lat="21.0"/>
<l c="cah" n="Cahuilla" lng="-116.25" lat="33.5"/>
<l c="cyv" n="Cayuvava" lng="-65.5" lat="-13.5"/>
<l c="cha" n="Chamorro" lng="144.75" lat="13.45"/>
<l c="cuu" n="Chuukese" lng="151.75" lat="7.33333333333"/>
<l c="chv" n="Chuvash" lng="47.5" lat="55.5"/>
<l c="cmn" n="Comanche" lng="-101.5" lat="33.5"/>
<l c="cre" n="Cree (Plains)" lng="-110.0" lat="54.0"/>
<l c="dam" n="Damana" lng="-73.5" lat="11.0"/>
<l c="eng" n="English" lng="0.0" lat="52.0"/>
<l c="eve" n="Evenki" lng="125.0" lat="56.0"/>
<l c="ewe" n="Ewe" lng="0.416666666667" lat="6.33333333333"/>
<l c="fij" n="Fijian" lng="178.0" lat="-17.8333333333"/>
<l c="fin" n="Finnish" lng="25.0" lat="62.0"/>
<l c="fre" n="French" lng="2.0" lat="48.0"/>
<l c="fur" n="Fur" lng="25.0" lat="13.5"/>
<l c="gar" n="Garo" lng="90.5" lat="25.6666666667"/>
<l c="ger" n="German" lng="10.0" lat="52.0"/>
<l c="goa" n="Goajiro" lng="-72.0" lat="12.0"/>
<l c="grk" n="Greek (Modern)" lng="22.0" lat="39.0"/>
<l c="gua" n="Guaraní" lng="-56.0" lat="-26.0"/>
<l c="gur" n="Gurung" lng="84.3333333333" lat="28.3333333333"/>
<l c="hai" n="Haida" lng="-132.0" lat="53.0"/>
<l c="hau" n="Hausa" lng="7.0" lat="12.0"/>
<l c="heb" n="Hebrew (Modern)" lng="34.8333333333" lat="31.5"/>
<l c="hin" n="Hindi" lng="77.0" lat="25.0"/>
<l c="hmo" n="Hmong Njua" lng="105.0" lat="28.0"/>
<l c="hlp" n="Hualapai" lng="-113.75" lat="35.5"/>
<l c="hun" n="Hungarian" lng="20.0" lat="47.0"/>
<l c="hzb" n="Hunzib" lng="46.25" lat="42.1666666667"/>
<l c="hup" n="Hupa" lng="-123.666666667" lat="41.0833333333"/>
<l c="ika" n="Ika" lng="-73.75" lat="10.6666666667"/>
<l c="ind" n="Indonesian" lng="106.0" lat="0.0"/>
<l c="irq" n="Iraqw" lng="35.5" lat="-4.0"/>
<l c="jpn" n="Japanese" lng="140.0" lat="37.0"/>
<l c="jaq" n="Jaqaru" lng="-76.0" lat="-13.0"/>
<l c="kab" n="Kabardian" lng="43.5" lat="43.5"/>
<l c="knd" n="Kannada" lng="76.0" lat="14.0"/>
<l c="knr" n="Kanuri" lng="13.0" lat="12.0"/>
<l c="krk" n="Karok" lng="-123.0" lat="41.6666666667"/>
<l c="kyl" n="Kayah Li (Eastern)" lng="97.5" lat="19.0"/>
<l c="ket" n="Ket" lng="87.0" lat="64.0"/>
<l c="khl" n="Khalaj" lng="50.0" lat="35.0"/>
<l c="kha" n="Khalkha" lng="105.0" lat="47.0"/>
<l c="kty" n="Khanty" lng="65.0" lat="65.0"/>
<l c="khm" n="Khmer" lng="105.0" lat="12.5"/>
<l c="klv" n="Kilivila" lng="151.083333333" lat="-8.5"/>
<l c="krb" n="Kiribati" lng="173.0" lat="1.33333333333"/>
<l c="koa" n="Koasati" lng="-85.1666666667" lat="34.8333333333"/>
<l c="kor" n="Korean" lng="128.0" lat="37.5"/>
<l c="kfe" n="Koromfe" lng="-0.916666666667" lat="14.25"/>
<l c="kse" n="Koyraboro Senni" lng="0.0" lat="16.0"/>
<l c="knm" n="Kunama" lng="37.0" lat="14.5"/>
<l c="kut" n="Kutenai" lng="-116.0" lat="49.5"/>
<l c="lak" n="Lak" lng="47.1666666667" lat="42.1666666667"/>
<l c="lkt" n="Lakhota" lng="-101.833333333" lat="43.8333333333"/>
<l c="lan" n="Lango" lng="33.0" lat="2.16666666667"/>
<l c="lat" n="Latvian" lng="24.0" lat="57.0"/>
<l c="lav" n="Lavukaleve" lng="159.2" lat="-9.08333333333"/>
<l c="leg" n="Lega" lng="27.1666666667" lat="-2.83333333333"/>
<l c="luv" n="Luvale" lng="22.0" lat="-12.0"/>
<l c="mal" n="Malagasy" lng="47.0" lat="-20.0"/>
<l c="mnd" n="Mandarin" lng="110.0" lat="34.0"/>
<l c="mao" n="Maori" lng="176.0" lat="-40.0"/>
<l c="map" n="Mapudungun" lng="-72.0" lat="-38.0"/>
<l c="msl" n="Masalit" lng="22.0" lat="13.3333333333"/>
<l c="nht" n="Nahuatl (Tetelcingo)" lng="-99.0" lat="19.6666666667"/>
<l c="kho" n="Nama" lng="18.0" lat="-25.5"/>
<l c="nav" n="Navajo" lng="-108.0" lat="36.1666666667"/>
<l c="ndy" n="Ndyuka" lng="-54.5" lat="4.5"/>
<l c="ntu" n="Nenets" lng="76.0" lat="70.0"/>
<l c="nez" n="Nez Perce" lng="-116.0" lat="46.0"/>
<l c="niv" n="Nivkh" lng="142.0" lat="53.3333333333"/>
<l c="nko" n="Nkore-Kiga" lng="29.8333333333" lat="-0.916666666667"/>
<l c="noo" n="Noon" lng="-16.8333333333" lat="14.8333333333"/>
<l c="nbd" n="Nubian (Dongolese)" lng="30.75" lat="18.25"/>
<l c="ond" n="Oneida" lng="-75.6666666667" lat="43.0"/>
<l c="orh" n="Oromo (Harar)" lng="42.0" lat="9.0"/>
<l c="pai" n="Paiwan" lng="120.833333333" lat="22.5"/>
<l c="prs" n="Persian" lng="54.0" lat="32.0"/>
<l c="poh" n="Pohnpeian" lng="158.25" lat="6.88333333333"/>
<l c="pme" n="Pomo (Eastern)" lng="-122.666666667" lat="39.0"/>
<l c="qim" n="Quechua (Imbabura)" lng="-78.0" lat="0.333333333333"/>
<l c="qui" n="Quileute" lng="-124.25" lat="47.9166666667"/>
<l c="rap" n="Rapanui" lng="-109.366666667" lat="-27.1166666667"/>
<l c="rus" n="Russian" lng="38.0" lat="56.0"/>
<l c="sah" n="Sahu" lng="127.5" lat="1.16666666667"/>
<l c="san" n="Sango" lng="18.0" lat="5.0"/>
<l c="sap" n="Sapuan" lng="106.833333333" lat="15.1666666667"/>
<l c="sla" n="Slave" lng="-125.0" lat="67.0"/>
<l c="so" n="So" lng="34.75" lat="2.58333333333"/>
<l c="sou" n="Sorbian (Upper)" lng="14.5" lat="51.8333333333"/>
<l c="spa" n="Spanish" lng="-4.0" lat="40.0"/>
<l c="swa" n="Swahili" lng="39.0" lat="-6.5"/>
<l c="tab" n="Taba" lng="127.5" lat="0.0"/>
<l c="tag" n="Tagalog" lng="121.0" lat="15.0"/>
<l c="twe" n="Tarahumara (Western)" lng="-108.0" lat="27.5"/>
<l c="tel" n="Telugu" lng="79.0" lat="16.0"/>
<l c="tha" n="Thai" lng="101.0" lat="16.0"/>
<l c="tli" n="Tlingit" lng="-135.0" lat="59.0"/>
<l c="tug" n="Tuareg (Ahaggar)" lng="6.0" lat="23.0"/>
<l c="tuk" n="Tukang Besi" lng="123.5" lat="-5.5"/>
<l c="tur" n="Turkish" lng="35.0" lat="39.0"/>
<l c="vie" n="Vietnamese" lng="106.5" lat="10.5"/>
<l c="yag" n="Yagua" lng="-72.0" lat="-3.5"/>
<l c="ykt" n="Yakut" lng="130.0" lat="62.0"/>
<l c="yko" n="Yukaghir (Kolyma)" lng="150.833333333" lat="65.75"/>
<l c="zul" n="Zulu" lng="30.0" lat="-30.0"/>
</v>
<v numeric="2" description="Hybrid vigesimal-decimal" icon_id="cff66ff" icon_url="https://wals.info/clld-static/icons/cff66ff.png" zindex="0">
<l c="abk" n="Abkhaz" lng="41.0" lat="43.0833333333"/>
<l c="bsq" n="Basque" lng="-3.0" lat="43.0"/>
<l c="bur" n="Burushaski" lng="74.5" lat="36.5"/>
<l c="cle" n="Chinantec (Lealao)" lng="-95.9166666667" lat="17.3333333333"/>
<l c="dsh" n="Danish" lng="10.0" lat="56.0"/>
<l c="dio" n="Diola-Fogny" lng="-16.25" lat="13.0"/>
<l c="fum" n="Fulfulde (Maasina)" lng="-5.0" lat="15.0"/>
<l c="geo" n="Georgian" lng="44.0" lat="42.0"/>
<l c="gol" n="Gola" lng="-10.8333333333" lat="7.25"/>
<l c="grw" n="Greenlandic (West)" lng="-51.0" lat="64.0"/>
<l c="hve" n="Huave (San Mateo del Mar)" lng="-95.0" lat="16.2166666667"/>
<l c="ing" n="Ingush" lng="45.0833333333" lat="43.1666666667"/>
<l c="iri" n="Irish" lng="-8.0" lat="53.0"/>
<l c="jak" n="Jakaltek" lng="-91.6666666667" lat="15.6666666667"/>
<l c="lez" n="Lezgian" lng="47.8333333333" lat="41.6666666667"/>
<l c="mei" n="Meithei" lng="94.0" lat="24.75"/>
<l c="mxa" n="Mixtec (Atatlahuca)" lng="-97.75" lat="17.0"/>
<l c="mxc" n="Mixtec (Chalcatongo)" lng="-97.5833333333" lat="17.05"/>
<l c="nsz" n="Nahuatl (Sierra de Zacapoaxtla)" lng="-97.3333333333" lat="19.5833333333"/>
<l c="otm" n="Otomí (Mezquital)" lng="-99.1666666667" lat="20.1666666667"/>
<l c="tsz" n="Tsez" lng="45.75" lat="42.25"/>
<l c="yaq" n="Yaqui" lng="-110.25" lat="27.5"/>
</v>
<v numeric="3" description="Pure vigesimal" icon_id="cdd0000" icon_url="https://wals.info/clld-static/icons/cdd0000.png" zindex="0">
<l c="ain" n="Ainu" lng="143.0" lat="43.0"/>
<l c="ala" n="Alamblak" lng="143.333333333" lat="-4.66666666667"/>
<l c="adk" n="Andoke" lng="-72.0" lat="-0.666666666667"/>
<l c="car" n="Carib" lng="-56.0" lat="5.5"/>
<l c="chk" n="Chukchi" lng="-173.0" lat="67.0"/>
<l c="dag" n="Daga" lng="149.333333333" lat="-10.0"/>
<l c="dre" n="Drehu" lng="167.25" lat="-21.0"/>
<l c="igb" n="Igbo" lng="7.33333333333" lat="6.0"/>
<l c="kan" n="Kana" lng="7.41666666667" lat="4.75"/>
<l c="kro" n="Krongo" lng="30.0" lat="10.5"/>
<l c="ara" n="Lokono" lng="-55.1666666667" lat="5.5"/>
<l c="mmb" n="Mangap-Mbula" lng="148.083333333" lat="-5.66666666667"/>
<l c="tam" n="Tamang (Eastern)" lng="85.666666666667" lat="27.5"/>
<l c="taw" n="Tawala" lng="150.666666667" lat="-10.3333333333"/>
<l c="wra" n="Warao" lng="-61.6666666667" lat="9.33333333333"/>
<l c="yim" n="Yimas" lng="143.55" lat="-4.66666666667"/>
<l c="yor" n="Yoruba" lng="4.33333333333" lat="8.0"/>
<l c="yct" n="Yucatec" lng="-89.0" lat="20.0"/>
<l c="ypk" n="Yup&#39;ik (Central)" lng="-160.0" lat="59.5"/>
<l c="zqc" n="Zoque (Copainalá)" lng="-93.25" lat="17.0"/>
</v>
<v numeric="4" description="Other base" icon_id="ccccccc" icon_url="https://wals.info/clld-static/icons/ccccccc.png" zindex="0">
<l c="eka" n="Ekari" lng="135.5" lat="-3.83333333333"/>
<l c="emc" n="Embera Chami" lng="-76.0" lat="5.0"/>
<l c="nti" n="Ngiti" lng="30.25" lat="1.33333333333"/>
<l c="sup" n="Supyire" lng="-5.58333333333" lat="11.5"/>
<l c="tms" n="Tommo So" lng="-3.0" lat="15.0"/>
</v>
<v numeric="5" description="Extended body-part system" icon_id="cffff00" icon_url="https://wals.info/clld-static/icons/cffff00.png" zindex="0">
<l c="eip" n="Eipo" lng="140.083333333" lat="-4.33333333333"/>
<l c="har" n="Haruai" lng="144.166666667" lat="-5.08333333333"/>
<l c="kob" n="Kobon" lng="144.333333333" lat="-5.16666666667"/>
<l c="una" n="Una" lng="140.0" lat="-4.66666666667"/>
</v>
<v numeric="6" description="Restricted" icon_id="cffffff" icon_url="https://wals.info/clld-static/icons/cffffff.png" zindex="0">
<l c="xoo" n="!Xóõ" lng="21.5" lat="-24.0"/>
<l c="acg" n="Achagua" lng="-72.25" lat="4.41666666667"/>
<l c="ana" n="Araona" lng="-67.75" lat="-12.3333333333"/>
<l c="awp" n="Awa Pit" lng="-78.25" lat="1.5"/>
<l c="brs" n="Barasano" lng="-70.6666666667" lat="-0.166666666667"/>
<l c="bae" n="Baré" lng="-67.0" lat="1.0"/>
<l c="goo" n="Gooniyandi" lng="126.333333333" lat="-18.3333333333"/>
<l c="hix" n="Hixkaryana" lng="-59.0" lat="-1.0"/>
<l c="hpd" n="Hup" lng="-69.25" lat="0.166666666667"/>
<l c="imo" n="Imonda" lng="141.166666667" lat="-3.33333333333"/>
<l c="kay" n="Kayardild" lng="139.5" lat="-17.05"/>
<l c="myi" n="Mangarrayi" lng="133.5" lat="-14.6666666667"/>
<l c="mrt" n="Martuthunira" lng="116.5" lat="-20.8333333333"/>
<l c="prh" n="Pirahã" lng="-62.0" lat="-7.0"/>
<l c="pit" n="Pitjantjatjara" lng="130.0" lat="-26.0"/>
<l c="ram" n="Rama" lng="-83.75" lat="11.75"/>
<l c="war" n="Wari&#39;" lng="-65.0" lat="-11.3333333333"/>
<l c="wsk" n="Waskia" lng="146.0" lat="-4.5"/>
<l c="wch" n="Wichí" lng="-62.5833333333" lat="-22.5"/>
<l c="yid" n="Yidiny" lng="145.75" lat="-17.0"/>
</v>
</feature>
"""

# =============================================================================
# REFUGIA GEOGRAPHIC DEFINITIONS
# =============================================================================

def classify_region(lat: float, lng: float) -> str:
    """
    Classify a language's location into a region.
    
    Refugia definitions:
    - Americas: longitude < -30°
    - Sahul: longitude > 110° AND latitude < 3°, 
             with additional restriction that languages between 
             latitudes -11° and 3° must have longitude > 125°
             (to exclude Sulawesi, Lesser Sundas, etc.)
    - Caucasus: 37° < latitude < 45° AND 37° < longitude < 50°
    
    Returns: 'americas', 'sahul', 'caucasus', or 'non_refugia'
    """
    # Americas
    if lng < -30:
        return 'americas'
    
    # Caucasus
    if 37 < lat < 45 and 37 < lng < 50:
        return 'caucasus'
    
    # Sahul (with Wallacea exclusion)
    if lng > 110 and lat < 3:
        # Additional check for western Wallacea exclusion
        if -11 < lat < 3:
            if lng > 125:
                return 'sahul'
            else:
                return 'non_refugia'
        else:
            return 'sahul'
    
    return 'non_refugia'


def is_refugia(lat: float, lng: float) -> bool:
    """Returns True if the location is in any refugia region."""
    return classify_region(lat, lng) != 'non_refugia'

# =============================================================================
# XML PARSING
# =============================================================================

def parse_wals_xml(xml_string: str) -> Optional[FeatureData]:
    """
    Parse WALS XML data into structured format.
    
    Args:
        xml_string: Raw XML string from WALS
        
    Returns:
        FeatureData object or None if parsing fails
    """
    # Clean up the XML string
    xml_string = xml_string.strip()
    
    # Skip if it's just a placeholder comment
    if xml_string.startswith('<!--') or not xml_string or '<feature' not in xml_string:
        return None
    
    # Handle HTML entities that might cause issues
    # First, protect already-escaped ampersands
    xml_string = xml_string.replace('&amp;', '__AMP__')
    # Escape bare ampersands
    xml_string = xml_string.replace('&', '&amp;')
    # Restore already-escaped ones
    xml_string = xml_string.replace('__AMP__', '&amp;')
    # Handle numeric character references
    xml_string = xml_string.replace('&amp;#39;', "'")
    xml_string = xml_string.replace('&#39;', "'")
    
    try:
        root = ET.fromstring(xml_string)
    except ET.ParseError as e:
        print(f"XML Parse Error: {e}")
        print("First 500 chars of input:")
        print(xml_string[:500])
        return None
    
    feature_id = root.get('number', 'Unknown')
    feature_name = root.get('name', 'Unknown')
    
    languages = []
    
    for value_elem in root.findall('v'):
        numeric_val = int(value_elem.get('numeric', 0))
        description = value_elem.get('description', '')
        
        for lang_elem in value_elem.findall('l'):
            code = lang_elem.get('c', '')
            name = lang_elem.get('n', '')
            lat_str = lang_elem.get('lat', '0')
            lng_str = lang_elem.get('lng', '0')
            
            try:
                lat = float(lat_str)
                lng = float(lng_str)
            except ValueError:
                print(f"Warning: Could not parse coordinates for {name} ({code})")
                continue
            
            languages.append(Language(
                code=code,
                name=name,
                latitude=lat,
                longitude=lng,
                value=numeric_val,
                description=description
            ))
    
    return FeatureData(
        feature_id=feature_id,
        feature_name=feature_name,
        languages=languages
    )

# =============================================================================
# STATISTICAL CALCULATIONS
# =============================================================================

def calculate_baseline(all_languages: List[Language]) -> Dict[str, any]:
    """
    Calculate baseline statistics: what percentage of all languages
    fall into each region?
    """
    region_counts = defaultdict(int)
    
    for lang in all_languages:
        region = classify_region(lang.latitude, lang.longitude)
        region_counts[region] += 1
    
    total = len(all_languages)
    refugia_count = sum(region_counts[r] for r in ['americas', 'sahul', 'caucasus'])
    
    return {
        'total': total,
        'americas': region_counts['americas'],
        'sahul': region_counts['sahul'],
        'caucasus': region_counts['caucasus'],
        'non_refugia': region_counts['non_refugia'],
        'refugia_total': refugia_count,
        'refugia_percentage': 100 * refugia_count / total if total > 0 else 0,
        'region_counts': dict(region_counts)
    }


def calculate_enrichment(
    target_languages: List[Language],
    baseline_refugia_pct: float
) -> Dict[str, any]:
    """
    Calculate enrichment statistics for a subset of languages.
    
    Args:
        target_languages: Languages with the feature of interest
        baseline_refugia_pct: Baseline percentage of all languages in refugia
        
    Returns:
        Dictionary with enrichment statistics
    """
    region_counts = defaultdict(int)
    
    for lang in target_languages:
        region = classify_region(lang.latitude, lang.longitude)
        region_counts[region] += 1
    
    total = len(target_languages)
    refugia_count = sum(region_counts[r] for r in ['americas', 'sahul', 'caucasus'])
    
    refugia_pct = 100 * refugia_count / total if total > 0 else 0
    enrichment = refugia_pct / baseline_refugia_pct if baseline_refugia_pct > 0 else 0
    
    return {
        'total': total,
        'americas': region_counts['americas'],
        'sahul': region_counts['sahul'],
        'caucasus': region_counts['caucasus'],
        'non_refugia': region_counts['non_refugia'],
        'refugia_total': refugia_count,
        'refugia_percentage': refugia_pct,
        'non_refugia_percentage': 100 - refugia_pct,
        'enrichment_factor': enrichment,
        'region_counts': dict(region_counts)
    }


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance between two points in kilometers.
    """
    R = 6371  # Earth's radius in km
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = (math.sin(delta_lat / 2) ** 2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


def compute_spatial_weights(
    languages: List[Language],
    k: int = 5,
    inverse_distance: bool = True
) -> List[List[float]]:
    """
    Compute spatial weights matrix using k-nearest neighbors.
    
    Args:
        languages: List of Language objects
        k: Number of nearest neighbors
        inverse_distance: If True, weight by inverse distance; if False, binary weights
        
    Returns:
        Row-standardized weights matrix
    """
    n = len(languages)
    weights = [[0.0] * n for _ in range(n)]
    
    for i in range(n):
        # Calculate distances to all other languages
        distances = []
        for j in range(n):
            if i != j:
                dist = haversine_distance(
                    languages[i].latitude, languages[i].longitude,
                    languages[j].latitude, languages[j].longitude
                )
                distances.append((j, dist))
        
        # Sort by distance and take k nearest
        distances.sort(key=lambda x: x[1])
        neighbors = distances[:k]
        
        # Assign weights
        if inverse_distance:
            # Inverse distance weights
            for j, dist in neighbors:
                weights[i][j] = 1.0 / max(dist, 0.1)  # Avoid division by zero
        else:
            # Binary weights
            for j, dist in neighbors:
                weights[i][j] = 1.0
    
    # Row-standardize
    for i in range(n):
        row_sum = sum(weights[i])
        if row_sum > 0:
            for j in range(n):
                weights[i][j] /= row_sum
    
    return weights


def calculate_morans_i(
    languages: List[Language],
    values: List[int],
    weights: List[List[float]]
) -> Tuple[float, float, float]:
    """
    Calculate Moran's I statistic for spatial autocorrelation.
    
    Args:
        languages: List of Language objects
        values: Binary values (0 or 1) for each language
        weights: Spatial weights matrix
        
    Returns:
        Tuple of (Moran's I, z-score, p-value)
    """
    n = len(values)
    if n < 3:
        return (0.0, 0.0, 1.0)
    
    # Mean
    mean_val = sum(values) / n
    
    # Variance terms
    deviations = [v - mean_val for v in values]
    sum_sq_dev = sum(d ** 2 for d in deviations)
    
    if sum_sq_dev == 0:
        return (0.0, 0.0, 1.0)
    
    # Calculate Moran's I numerator
    numerator = 0.0
    W = 0.0  # Sum of all weights
    
    for i in range(n):
        for j in range(n):
            if i != j:
                numerator += weights[i][j] * deviations[i] * deviations[j]
                W += weights[i][j]
    
    if W == 0:
        return (0.0, 0.0, 1.0)
    
    # Moran's I
    I = (n / W) * (numerator / sum_sq_dev)
    
    # Expected value under null hypothesis
    E_I = -1.0 / (n - 1)
    
    # Variance calculation under randomization assumption
    S1 = 0.0
    S2 = 0.0
    
    for i in range(n):
        row_sum = sum(weights[i])
        col_sum = sum(weights[j][i] for j in range(n))
        S2 += (row_sum + col_sum) ** 2
        for j in range(n):
            S1 += (weights[i][j] + weights[j][i]) ** 2
    
    S1 /= 2
    
    # Kurtosis of the values
    m2 = sum_sq_dev / n
    m4 = sum(d ** 4 for d in deviations) / n
    b2 = m4 / (m2 ** 2) if m2 > 0 else 3.0
    
    # Variance calculation (under randomization)
    A = n * ((n**2 - 3*n + 3) * S1 - n * S2 + 3 * W**2)
    B = b2 * ((n**2 - n) * S1 - 2*n * S2 + 6 * W**2)
    C = (n - 1) * (n - 2) * (n - 3) * W**2
    
    if C == 0:
        return (I, 0.0, 1.0)
    
    var_I = (A - B) / C - E_I**2
    
    if var_I <= 0:
        return (I, 0.0, 1.0)
    
    # Z-score
    z = (I - E_I) / math.sqrt(var_I)
    
    # P-value (two-tailed, using normal approximation)
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    
    return (I, z, p)


def permutation_test(
    languages: List[Language],
    values: List[int],
    weights: List[List[float]],
    n_permutations: int = 999
) -> Tuple[float, float]:
    """
    Perform permutation test for Moran's I.
    
    Returns:
        Tuple of (observed Moran's I, empirical p-value)
    """
    observed_I, _, _ = calculate_morans_i(languages, values, weights)
    
    more_extreme = 0
    
    for _ in range(n_permutations):
        # Randomly shuffle values
        shuffled_values = values.copy()
        random.shuffle(shuffled_values)
        
        perm_I, _, _ = calculate_morans_i(languages, shuffled_values, weights)
        
        if abs(perm_I) >= abs(observed_I):
            more_extreme += 1
    
    p_value = (more_extreme + 1) / (n_permutations + 1)
    
    return (observed_I, p_value)

# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def analyze_feature(
    feature_data: FeatureData,
    target_values: List[int],
    feature_label: str,
    baseline_stats: Dict[str, any],
    k_neighbors: int = 5,
    run_permutation: bool = False,
    n_permutations: int = 999
) -> Dict[str, any]:
    """
    Perform complete analysis for a single feature.
    """
    # Filter to target languages
    target_langs = [l for l in feature_data.languages if l.value in target_values]
    
    # Binary values for all languages (1 if target, 0 otherwise)
    binary_values = [1 if l.value in target_values else 0 for l in feature_data.languages]
    
    # Enrichment analysis
    enrichment = calculate_enrichment(target_langs, baseline_stats['refugia_percentage'])
    
    # Spatial weights and Moran's I
    if len(feature_data.languages) >= 5:
        weights = compute_spatial_weights(feature_data.languages, k=k_neighbors)
        morans_i, z_score, p_value = calculate_morans_i(
            feature_data.languages, binary_values, weights
        )
        
        # Optional permutation test
        if run_permutation and len(target_langs) >= 3:
            _, perm_p = permutation_test(
                feature_data.languages, binary_values, weights, n_permutations
            )
        else:
            perm_p = None
    else:
        morans_i, z_score, p_value = 0.0, 0.0, 1.0
        perm_p = None
    
    return {
        'feature_id': feature_data.feature_id,
        'feature_name': feature_data.feature_name,
        'feature_label': feature_label,
        'target_values': target_values,
        'total_languages': len(feature_data.languages),
        'target_count': len(target_langs),
        'target_percentage': 100 * len(target_langs) / len(feature_data.languages),
        'enrichment': enrichment,
        'morans_i': morans_i,
        'z_score': z_score,
        'p_value': p_value,
        'permutation_p': perm_p,
        'target_languages': target_langs
    }


def print_results(results: Dict[str, any], baseline: Dict[str, any]):
    """Print formatted results for a single feature analysis."""
    print("\n" + "=" * 70)
    print(f"FEATURE: {results['feature_label']}")
    print(f"WALS Chapter: {results['feature_id']} - {results['feature_name']}")
    print("=" * 70)
    
    print(f"\nSample Size:")
    print(f"  Total languages in chapter: {results['total_languages']}")
    print(f"  Languages with target feature: {results['target_count']} ({results['target_percentage']:.1f}%)")
    
    print(f"\nRegional Distribution:")
    e = results['enrichment']
    print(f"  Americas:    {e['americas']:3d} ({100*e['americas']/e['total']:.1f}%)" if e['total'] > 0 else "  Americas:    0")
    print(f"  Sahul:       {e['sahul']:3d} ({100*e['sahul']/e['total']:.1f}%)" if e['total'] > 0 else "  Sahul:       0")
    print(f"  Caucasus:    {e['caucasus']:3d} ({100*e['caucasus']/e['total']:.1f}%)" if e['total'] > 0 else "  Caucasus:    0")
    print(f"  Non-refugia: {e['non_refugia']:3d} ({100*e['non_refugia']/e['total']:.1f}%)" if e['total'] > 0 else "  Non-refugia: 0")
    
    print(f"\nEnrichment Analysis:")
    print(f"  Baseline refugia %: {baseline['refugia_percentage']:.1f}%")
    print(f"  Feature refugia %:  {e['refugia_percentage']:.1f}%")
    print(f"  Enrichment factor:  {e['enrichment_factor']:.2f}x")
    
    print(f"\nSpatial Autocorrelation (Moran's I):")
    print(f"  Moran's I: {results['morans_i']:.4f}")
    print(f"  Z-score:   {results['z_score']:.2f}")
    print(f"  P-value:   {results['p_value']:.6f}")
    if results['permutation_p'] is not None:
        print(f"  Permutation P-value: {results['permutation_p']:.4f}")
    
    # List languages if small enough
    if len(results['target_languages']) <= 25:
        print(f"\nTarget Languages ({len(results['target_languages'])} total):")
        for lang in sorted(results['target_languages'], key=lambda x: x.name):
            region = classify_region(lang.latitude, lang.longitude)
            print(f"  {lang.name} ({lang.code}): {region}")


def generate_table_1(all_results: List[Dict], baseline: Dict) -> str:
    """Generate formatted table similar to Table 1 in the paper."""
    lines = []
    lines.append("\n" + "=" * 105)
    lines.append("TABLE 1: Summary Statistics for All Features")
    lines.append("=" * 105)
    lines.append(f"{'Feature Name':<40} {'% Refugia':>10} {'% Non-Ref':>10} {'Enrichment':>12} {'Moran I':>10} {'P-value':>12}")
    lines.append("-" * 105)
    
    # Baseline row
    lines.append(f"{'Total (Global Baseline)':<40} {baseline['refugia_percentage']:>9.1f}% {100-baseline['refugia_percentage']:>9.1f}% {'1.00x':>12} {'~0':>10} {'N/A':>12}")
    lines.append("-" * 105)
    
    # Sort by enrichment factor
    sorted_results = sorted(all_results, key=lambda x: x['enrichment']['enrichment_factor'])
    
    for r in sorted_results:
        e = r['enrichment']
        if r['p_value'] < 0.001:
            p_str = "< 0.001"
        else:
            p_str = f"{r['p_value']:.4f}"
        lines.append(
            f"{r['feature_label']:<40} {e['refugia_percentage']:>9.1f}% {e['non_refugia_percentage']:>9.1f}% "
            f"{e['enrichment_factor']:>11.2f}x {r['morans_i']:>10.4f} {p_str:>12}"
        )
    
    lines.append("=" * 105)
    return "\n".join(lines)


def generate_detailed_regional_table(all_results: List[Dict]) -> str:
    """Generate detailed regional breakdown table."""
    lines = []
    lines.append("\n" + "=" * 90)
    lines.append("DETAILED REGIONAL BREAKDOWN")
    lines.append("=" * 90)
    lines.append(f"{'Feature':<35} {'Americas':>12} {'Sahul':>12} {'Caucasus':>12} {'Non-Ref':>12}")
    lines.append("-" * 90)
    
    for r in sorted(all_results, key=lambda x: x['enrichment']['enrichment_factor'], reverse=True):
        e = r['enrichment']
        total = e['total']
        if total > 0:
            lines.append(
                f"{r['feature_label'][:35]:<35} "
                f"{e['americas']:>5} ({100*e['americas']/total:>4.1f}%) "
                f"{e['sahul']:>5} ({100*e['sahul']/total:>4.1f}%) "
                f"{e['caucasus']:>5} ({100*e['caucasus']/total:>4.1f}%) "
                f"{e['non_refugia']:>5} ({100*e['non_refugia']/total:>4.1f}%)"
            )
    
    lines.append("=" * 90)
    return "\n".join(lines)

# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def main():
    """Run the complete refugia analysis."""
    print("=" * 70)
    print("REFUGIA LINGUISTIC ANALYSIS")
    print("Statistical Analysis of Feature Distributions")
    print("=" * 70)
    
    # Parse all datasets
    datasets = {}
    
    print("\n[1] PARSING WALS XML DATA")
    print("-" * 40)
    
    data_1a = parse_wals_xml(WALS_1A_CONSONANTS)
    if data_1a:
        datasets['1A'] = data_1a
        print(f"  ✓ 1A (Consonant Inventories): {len(data_1a.languages)} languages")
    else:
        print("  ✗ 1A: Not loaded (placeholder or invalid data)")
    
    data_2a = parse_wals_xml(WALS_2A_VOWELS)
    if data_2a:
        datasets['2A'] = data_2a
        print(f"  ✓ 2A (Vowel Quality Inventories): {len(data_2a.languages)} languages")
    else:
        print("  ✗ 2A: Not loaded (placeholder or invalid data)")
    
    data_18a = parse_wals_xml(WALS_18A_CONSONANT_ABSENCES)
    if data_18a:
        datasets['18A'] = data_18a
        print(f"  ✓ 18A (Absence of Common Consonants): {len(data_18a.languages)} languages")
    else:
        print("  ✗ 18A: Not loaded (placeholder or invalid data)")
    
    data_131a = parse_wals_xml(WALS_131A_NUMERALS)
    if data_131a:
        datasets['131A'] = data_131a
        print(f"  ✓ 131A (Numeral Bases): {len(data_131a.languages)} languages")
    else:
        print("  ✗ 131A: Not loaded (placeholder or invalid data)")
    
    if not datasets:
        print("\n" + "!" * 70)
        print("ERROR: No data loaded!")
        print("Please paste your WALS XML data into the data variables at the top of the script.")
        print("!" * 70)
        return
    
    # Calculate baseline from combined unique languages
    print("\n[2] CALCULATING BASELINE STATISTICS")
    print("-" * 40)
    
    # Combine all unique languages across all datasets
    all_languages_dict = {}
    for feature_id, data in datasets.items():
        for lang in data.languages:
            # Use code + approximate coordinates as key to deduplicate
            key = (lang.code, round(lang.latitude, 2), round(lang.longitude, 2))
            if key not in all_languages_dict:
                all_languages_dict[key] = lang
    
    all_languages = list(all_languages_dict.values())
    baseline = calculate_baseline(all_languages)
    
    print(f"\nCombined unique languages across all chapters: {baseline['total']}")
    print(f"\nRegional distribution (BASELINE):")
    print(f"  Americas:    {baseline['americas']:4d} ({100*baseline['americas']/baseline['total']:5.1f}%)")
    print(f"  Sahul:       {baseline['sahul']:4d} ({100*baseline['sahul']/baseline['total']:5.1f}%)")
    print(f"  Caucasus:    {baseline['caucasus']:4d} ({100*baseline['caucasus']/baseline['total']:5.1f}%)")
    print(f"  Non-refugia: {baseline['non_refugia']:4d} ({100*baseline['non_refugia']/baseline['total']:5.1f}%)")
    print(f"\n  >>> REFUGIA TOTAL: {baseline['refugia_total']} ({baseline['refugia_percentage']:.2f}%) <<<")
    
    # Also compute per-chapter baselines
    print("\n[3] PER-CHAPTER BASELINES")
    print("-" * 40)
    chapter_baselines = {}
    for feature_id, data in sorted(datasets.items()):
        cb = calculate_baseline(data.languages)
        chapter_baselines[feature_id] = cb
        print(f"  {feature_id}: N={cb['total']:3d}, Refugia={cb['refugia_percentage']:.1f}%")
    
    # Run analyses for each feature
    print("\n[4] FEATURE ANALYSES")
    print("-" * 40)
    
    all_results = []
    
    # 1A: Small Consonant Inventories (value = 1)
    if '1A' in datasets:
        result = analyze_feature(
            datasets['1A'],
            target_values=[1],
            feature_label="Small Consonant Inventories (6-14)",
            baseline_stats=baseline
        )
        all_results.append(result)
        print_results(result, baseline)
    
    # 2A: Small Vowel Inventories (value = 1)
    if '2A' in datasets:
        result = analyze_feature(
            datasets['2A'],
            target_values=[1],
            feature_label="Small Vowel Quality Inventories (2-4)",
            baseline_stats=baseline
        )
        all_results.append(result)
        print_results(result, baseline)
    
    # 18A: Absence of Fricatives (value = 3)
    if '18A' in datasets:
        result = analyze_feature(
            datasets['18A'],
            target_values=[3],
            feature_label="Absence of Fricatives",
            baseline_stats=baseline
        )
        all_results.append(result)
        print_results(result, baseline)
    
    # 18A: Absence of Nasals (values = 4, 5, 6)
    if '18A' in datasets:
        result = analyze_feature(
            datasets['18A'],
            target_values=[4, 5, 6],
            feature_label="Absence of Nasals",
            baseline_stats=baseline
        )
        all_results.append(result)
        print_results(result, baseline)
    
    # 18A: Absence of Bilabials (values = 2, 5)
    if '18A' in datasets:
        result = analyze_feature(
            datasets['18A'],
            target_values=[2, 5],
            feature_label="Absence of Bilabials",
            baseline_stats=baseline
        )
        all_results.append(result)
        print_results(result, baseline)
    
    # 131A: Restricted Numeral Systems (value = 6)
    if '131A' in datasets:
        result = analyze_feature(
            datasets['131A'],
            target_values=[6],
            feature_label="Restricted Numeral Systems",
            baseline_stats=baseline
        )
        all_results.append(result)
        print_results(result, baseline)
    
    # Generate summary tables
    if all_results:
        print("\n[5] SUMMARY TABLES")
        print(generate_table_1(all_results, baseline))
        print(generate_detailed_regional_table(all_results))
    
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)
    main()
