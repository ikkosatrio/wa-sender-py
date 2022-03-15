from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import requests
import time
import datetime
from datetime import date
from datetime import datetime
from time import sleep
from time import gmtime, strftime
from pytz import timezone   
import pytz
import urllib
import urllib.parse
from urllib.parse import quote
import mysql.connector
import re
import locale
import os
import socket
import urllib.request

# VARIBLE  UNTUK OTOMATISASI JAWABAN DAN KONFIGURASI
codeurl = 'https://raw.githubusercontent.com/brekertabumi/kelas_wa/main/class_wa_bot.py'
variabel = urllib.request.urlopen(codeurl)
datavariabel = variabel.read()
exec(datavariabel)

kodePa = "PTA.Sby"
namapa = "Pengadilan Tinggi Agama Surabaya"
options = Options()
ua = UserAgent()
userAgent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"
options.add_argument(f'user-agent={userAgent}')

jkt = pytz.timezone('Asia/Jakarta')
sa_time = datetime.now(jkt)
jamSekarang = sa_time.strftime('%H')
def koneksisipp():
    dbsipp = mysql.connector.connect(host="101.50.1.15",user="ptasura1_pim2adit",passwd="Zmq=3knHNMCL",database="ptasura1_suramadu")
    return dbsipp
def koneksilocal():
    dblocal = mysql.connector.connect(host="101.50.1.15",user="ptasura1_pim2adit",passwd="Zmq=3knHNMCL",database="ptasura1_suramadu")
    return dblocal

koneksipp = koneksisipp()
if koneksipp.is_connected():
    print("Koneksi", "Koneksi ke SIPP Berhasil")
    koneksipp.close()
else :
    print("Koneksi", "Koneksi ke SIPP Gagal")

koneklocal = koneksilocal()
if koneklocal.is_connected():
    print("Koneksi", "Koneksi ke DB Local Berhasil")
    koneklocal.close()
else :
    print("Koneksi", "Koneksi DB Local Gagal")

chrome_options = Options()
browser = webdriver.Chrome(executable_path='C:/wa/chromedriver.exe', chrome_options=options)
browser.get('https://web.whatsapp.com')
sleep(30)


def element_presence(by, xpath, time):
    element_present = EC.presence_of_element_located((By.XPATH, xpath))
    WebDriverWait(browser, time).until(element_present)


def send_whatsapp_msg(no_wa, jawaban):
    browser.get("https://web.whatsapp.com/send?phone={}&source=&data=#".format(no_wa))
    try:
        WebDriverWait(browser, 3).until(EC.alert_is_present(), )
        browser.switch_to.alert.accept()
    except TimeoutException:
        pass

    try:
        text_box = browser.find_element_by_class_name(_TEXTBOX_)
        text_box.send_keys(jawaban)
        text_box.send_keys("\n")

    except Exception as e:
        pass

def number_format(num, places=0):
    return locale.format_string("%.*f", (places, num), True)



def cek_notif_outbox():
    print("Notif Outbox")
    try:
        koneklocal = koneksilocal()
        cursor_local_outbox = koneklocal.cursor()
        sql_local_outbox = "select `id`, `no_wa`, `isi_pesan`, `tgl_input`, `status`, `tgl_kirim` from outbox where status ='false' "
        cursor_local_outbox.execute(sql_local_outbox)
        results_outbox = cursor_local_outbox.fetchall()
        jumrowoutbox = cursor_local_outbox.rowcount
        # print(str(jumrowoutbox))
        if jumrowoutbox == 0:
            pass
        else:
            global data_outbox
            for data_outbox in results_outbox:
                id_outbox = data_outbox[0]
                no_wa = data_outbox[1]
                isi_pesan = data_outbox[2]
                tgl_input = data_outbox[3]
                # status = data_outbox[4]
                # tgl_kirim = data_outbox[5]
                jkt = pytz.timezone('Asia/Jakarta')
                tanggalkirim = datetime.now(jkt)
                jawaban = isi_pesan + " \n"
                print("Kirim Notif Outbox ke : " + no_wa)
                print(isi_pesan)

                browser.get("https://web.whatsapp.com/send?phone={}&source=&data=#".format(no_wa))
                try:
                    WebDriverWait(browser, 5).until(EC.alert_is_present(), )
                    browser.switch_to.alert.accept()
                except TimeoutException:
                    pass

                try:
                    text_box = browser.find_element_by_class_name(_TEXTBOX_)
                    #txt_box.send_keys(jawaban)
                    ganti = jawaban.replace("|", "~")
                    for part in ganti.split('~'):
                        text_box.send_keys(part)
                        action = webdriver.common.action_chains.ActionChains(browser)
                        action.key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).perform()
                    sleep(10)
                    text_box.send_keys(" \n")                   
                    sql_update_outbox = "update outbox set status ='true' , tgl_kirim =%s where id=%s "
                    cursor_local_outbox.execute(sql_update_outbox, (tanggalkirim, id_outbox,))
                    koneklocal.commit()


                    names = [namaakunparkircursor]  # akun parkir untuk cursor setelah eksekusi pesan
                    for name in names:
                        person = browser.find_element_by_xpath('//span[@title = "{}"]'.format(name))
                        person.click()

                except Exception as e:
                    pass
    finally:
        koneklocal.close()
        pass



def cek_notif_outbox_group():
    print("Notif Outbox_group")
    try:
        koneklocal = koneksilocal()
        cursor_local_outbox_group = koneklocal.cursor()
        sql_local_outbox_group = "select `id`, `nama_group`, `isi_pesan`, `tgl_input`, `status`, `tgl_kirim` from outbox_group where status ='false' "
        cursor_local_outbox_group.execute(sql_local_outbox_group)
        results_outbox_group = cursor_local_outbox_group.fetchall()
        jumrowoutbox_group = cursor_local_outbox_group.rowcount
        # print(str(jumrowoutbox))
        if jumrowoutbox_group == 0:
            pass
        else:
            global data_outbox_group
            for data_outbox_group in results_outbox_group:
                id_group = data_outbox_group[0]
                nama_group = data_outbox_group[1]
                isi_pesan = data_outbox_group[2]
                jkt = pytz.timezone('Asia/Jakarta')
                tanggalkirim_group = datetime.now(jkt)
                jawaban = isi_pesan + " \n"
                print("Kirim Notif Outbox ke Group : " + nama_group)
                namagroups = [nama_group]
                for name in namagroups:
                    kontak = browser.find_element_by_xpath('//span[@title = "{}"]'.format(name))
                    kontak.click()
                    sleep(3)
                    text_box = browser.find_element_by_class_name(_TEXTBOX_)
                    ganti = jawaban.replace("|", "~")
                    for part in ganti.split('~'):
                        text_box.send_keys(part)
                        action = webdriver.common.action_chains.ActionChains(browser)
                        action.key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).perform()

                    text_box.send_keys(" \n")

                    sql_update_outbox_group = "update outbox_group set status ='true' , tgl_kirim =%s where id=%s "
                    cursor_local_outbox_group.execute(sql_update_outbox_group, (tanggalkirim_group, id_group,))
                    koneklocal.commit()
                    sleep(3)

                    names = [namaakunparkircursor]  # akun parkir untuk cursor setelah eksekusi pesan
                    for name in names:
                        person = browser.find_element_by_xpath('//span[@title = "{}"]'.format(name))
                        person.click()
    except:
         pass
    # finally:
    #      koneklocal.close()

''' kumpulan fungsi reply otomatis '''


def _reply_sidang(pesan2):
    try:
        text_box = browser.find_element_by_class_name(_TEXTBOX_)
        pecah_perk = pesan2.split("/", 3)
        no_perk = pecah_perk[0]
        no_perk = no_perk.lstrip("0")
        jns_perk = pecah_perk[1].upper()
        jns_perk = jns_perk.replace("PDT.", "Pdt.")
        thn_perk = pecah_perk[2]
        no_perk_lengkap = no_perk + "/" + jns_perk + "/" + thn_perk + "/" + kodePa

        #CEK NOMOR PERKARA
        koneksipp = koneksisipp()
        cursor = koneksipp.cursor()
        sqlperkara = "SELECT * FROM perkara WHERE nomor_perkara = %s "
        cursor.execute(sqlperkara, (no_perk_lengkap,))
        results_perkara = cursor.fetchall()
        jumlahperkara = cursor.rowcount
        if jumlahperkara == 0: #PERKARA BELUM TERDAFTAR
            print("perkara belum terdaftar / nomor perkara salah")
            jawaban = "Nomor Perkara : *" + no_perk_lengkap + "* belum terdaftar, pastikan Anda memasukan nomor perkara dengan benar. " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "" + namapa + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*" + kodePa + "* \n"
            text_box.send_keys(jawaban)
        else: #PERKARA SUDAH TERDAFTAR
            print("perkara sudah terdaftar")
            global dataperkara
            for dataperkara in results_perkara:
                idperkara=dataperkara[0]
                jenisperkara=str(dataperkara[6])
                print("idperkara")
                print(idperkara)

            #CEK PUTUSAN
            sqlputusan = "SELECT A.tanggal_putusan, B.nama FROM perkara_putusan A, status_putusan B WHERE A.perkara_id = %s AND A.status_putusan_id=B.id"
            cursor.execute(sqlputusan, (idperkara,))
            results_putusan = cursor.fetchall()
            jumlahputusan = cursor.rowcount
            if jumlahputusan == 0: #BELUM PUTUS
                #CEK TANGGAL SIDANG
                print("belum putus")
                sqlsidang = "SELECT MAX(tanggal_sidang) as tgl_sidang,urutan,agenda FROM perkara_jadwal_sidang WHERE perkara_id = %s"
                cursor.execute(sqlsidang, (idperkara,))
                results_sidang = cursor.fetchall()
                jumlahsidang = cursor.rowcount
                if jumlahsidang == 0:  # BELUM ADA JADWAL SIDANG
                    print("belum ada jadwal sidang")
                    jawaban = "Nomor Perkara : *" + no_perk_lengkap + "* belum ada jadwal sidang, silahkan cek beberapa hari lagi. " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "" + namapa + "" + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*" + kodePa + "* \n"
                    text_box.send_keys(jawaban)
                else: #SUDAH ADA JADWAL SIDANG
                    print("sudah ada jadwal sidang")
                    global datasidang
                    for datasidang in results_sidang:
                        tanggalsidang = datasidang[0]
                        urutansidang = datasidang[1]
                        agendasidang = datasidang[2]

                    jkt = pytz.timezone('Asia/Jakarta')
                    tanggalsekarang = datetime.now(jkt)
                    tanggalsekarang = str(tanggalsekarang)
                    tanggalsekarang = tanggalsekarang[0:10]
                    tanggalsekarang = datetime.strptime(tanggalsekarang, '%Y-%m-%d').date()

                    if tanggalsidang >= tanggalsekarang: #ADA JADWAL SIDANG BARU SETELAH TANGGAL HARI INI
                        print("ada jadwal sidang baru")
                        jawaban = "Nomor Perkara : *" + no_perk_lengkap + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Tanggal Sidang : *" + str(
                            tanggalsidang) + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Sidang Ke : *" + str(
                            urutansidang) + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Agenda : *" + str(
                            agendasidang) + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "" + namapa + "" + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*" + kodePa + "* \n"
                        text_box.send_keys(jawaban)
                    else: #TANGGAL SIDANG SUDAH LEWAT DARI TANGGAL HARI INI
                        print("tidak ada jadwal sidang baru")
                        jawaban = "Nomor Perkara : *" + no_perk_lengkap + "* sidang terakhir tanggal *" + str(tanggalsidang) + "* , jadwal sidang berikutnya belum ditentukan oleh hakim, silahkan cek beberapa hari lagi. " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "" + namapa + "" + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*" + kodePa + "* \n"
                        text_box.send_keys(jawaban)

            else: #SUDAH PUTUS
                print("sudah putus")
                global dataputusan
                for dataputusan in results_putusan:
                    tanggalputusan = dataputusan[0]
                    jenisputusan = str(dataputusan[1])
                    print("jenisputusan")
                    print(jenisputusan)
                    print(jenisperkara)

                if jenisperkara == "Cerai Talak" and jenisputusan == "Dikabulkan": #JIKA PERKARA CERAI TALAK DAN PUTUSAN DIKABULKAN >> CEK JADWAL SIDANG IKRAR >> YAITU JADWAL SIDANG SETELAH TANGGAL PUTUS
                    # CEK TANGGAL SIDANG IKRAR
                    print("cerai talak dikabulkan")
                    sqlsidangikrar = "SELECT MAX(tanggal_sidang) as tgl_sidang,urutan,agenda FROM perkara_jadwal_sidang WHERE perkara_id = %s AND tanggal_sidang > %s"
                    cursor.execute(sqlsidangikrar, (idperkara, tanggalputusan,))
                    results_sidang_ikrar = cursor.fetchall()
                    jumlahsidangikrar = cursor.rowcount
                    if jumlahsidangikrar == 0:  # BELUM ADA JADWAL SIDANG IKRAR
                        print("belum ada jadwal sidang ikrar")
                        jawaban = "Nomor Perkara : *" + no_perk_lengkap + "* sudah putus tanggal *" + str(tanggalputusan) + "* , jadwal sidang ikrar belum ditentukan oleh hakim, silahkan cek beberapa hari lagi. " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "" + namapa + "" + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*" + kodePa + "* \n"
                        text_box.send_keys(jawaban)
                    else:  # SUDAH ADA JADWAL SIDANG IKRAR
                        global datasidangikrar
                        for datasidang in results_sidang_ikrar:
                            tanggalsidangikrar = datasidang[0]
                            urutansidang = datasidang[1]
                            agendasidang = datasidang[2]

                        jkt = pytz.timezone('Asia/Jakarta')
                        tanggalsekarang = datetime.now(jkt)
                        tanggalsekarang = str(tanggalsekarang)
                        tanggalsekarang = tanggalsekarang[0:10]
                        tanggalsekarang = datetime.strptime(tanggalsekarang, '%Y-%m-%d').date()
                        if tanggalsidangikrar >= tanggalsekarang:  # ADA JADWAL SIDANG IKRAR SETELAH TANGGAL HARI INI
                            print("ada jadwal sidang ikrar baru")
                            jawaban = "Nomor Perkara : *" + no_perk_lengkap + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Tanggal Sidang : *" + str(
                                tanggalsidangikrar) + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Sidang Ke : *" + str(
                                urutansidang) + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Agenda : *" + str(
                                agendasidang) + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "" + namapa + "" + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*" + kodePa + "* \n"
                            text_box.send_keys(jawaban)
                        else:  # TANGGAL SIDANG IKRAR SUDAH LEWAT DARI TANGGAL HARI INI
                            print("tanggal ikrar sudah lewat hari ini")
                            jawaban = "Nomor Perkara : *" + no_perk_lengkap + "* sidang ikrar terakhir tanggal *" + str(
                                tanggalsidangikrar) + "* , jika Anda pihak yang berperkara dan belum melaksanakan ikrar silahkan konfirmasi ke Kantor " + namapa + ". " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "" + namapa + "" + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*" + kodePa + "* \n"
                            text_box.send_keys(jawaban)

                else: #SELAIN PERKARA CERAI TALAK >> INFOKAN PERKARA SUDAH PUTUS
                    print("perkara sudah putus non CT")
                    jawaban = "Nomor Perkara : *" + no_perk_lengkap + "* tidak ada jadwal sidang baru, Perkara sudah putus pada saat sidang terakhir tanggal *" + str(tanggalputusan) + "* , jenis putusan *" + jenisputusan + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "" + namapa + "" + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*" + kodePa + "* \n"
                    text_box.send_keys(jawaban)


        koneksipp.close()

    except Exception as e:
        print(e)
        pass


def _reply_akta(pesan2,nomorhppihakfull):
    print("cek_akta")
    text_box = browser.find_element_by_class_name(_TEXTBOX_)
    koneksipp = koneksisipp()
    cursorakta = koneksipp.cursor()
    pecah_perk = pesan2.split("/", 3)
    no_perk = pecah_perk[0]
    no_perk = no_perk.lstrip("0")
    # jns_perk = pecah_perk[1][4:].upper()
    jns_perk = pecah_perk[1].upper()
    jns_perk = jns_perk.replace("PDT.", "Pdt.")
    thn_perk = pecah_perk[2]
    no_perk_lengkap = no_perk + "/" + jns_perk + "/" + thn_perk + "/" + kodePa
    sqlakta = "select a.perkara_id as perkaraid,a.pihak1_text,a.pihak2_text,b.perkara_id as perkaraid_akta, b.nomor_akta_cerai,b.tgl_akta_cerai as tgl_akta,a.proses_terakhir_text from perkara a left join perkara_akta_cerai b on a.perkara_id=b.perkara_id where a.perkara_id=(select perkara_id from perkara where nomor_perkara=%s)"
    cursorakta.execute(sqlakta, (no_perk_lengkap,))
    results = cursorakta.fetchall()
    jumrowac = cursorakta.rowcount
    print(str(jumrowac))
    if jumrowac == 0:
        jawaban = "Nomor Perkara: " + no_perk_lengkap + "  _Data tidak ditemukan di database_ \n"
        text_box.send_keys(jawaban)
    else:
        global dataac
        for dataac in results:
            nomorperkara = no_perk_lengkap
            cursorphone = koneksipp.cursor()
            sqltelepon = "select telepon from pihak where telepon=%s"
            cursorphone.execute(sqltelepon, (nomorhppihakfull,))
            hasilphone = cursorphone.fetchall()
            jumphone = cursorphone.rowcount
            if "0" in str(jumphone):
                namap = "_Disamarkan_"
                namat = "_Disamarkan_"
            else:
                namap = dataac[1]
                namat = dataac[2]

            nomoraktacerai = dataac[4]
            tglac = str(dataac[5])
            # print(tglac)
            if "None" in tglac:
                jawaban = "Nomor Perkara: " + nomorperkara + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Akta Cerai Belum Terbit* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Tahapan Proses Perkara : *" + \
                          dataac[6] + "* \n"
                text_box.send_keys(jawaban)
            else:
                jawaban = "*Nomor Perkara :* " + nomorperkara + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Nama P :* " + namap + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Nama T :* " + namat + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Nomor Akta Cerai :* " + nomoraktacerai + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Tgl Akta Cerai :* " + tglac + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_*Jika anda pihak berperkara pada perkara ini dan belum ambil akta cerai tersebut, silahkan diambil dengan membawa KTP asli pada hari & jam kerja.*_ \n"
                text_box.send_keys(jawaban)
                # print(jawaban)
    koneksipp.close()

def _reply_vakta(pesan2,no_hp,no_wa):
    print("cek_akta_kua_VAKTA")
    text_box = browser.find_element_by_class_name(_TEXTBOX_)

    koneklocal = koneksilocal()
    cursorlocal = koneklocal.cursor()
    sqllocal_cek_hp_kua = "select nama_instansi, nama, no_hp from " + namadatabaselocal + ".kua where no_hp =%s"
    cursorlocal.execute(sqllocal_cek_hp_kua, (no_hp,))
    result_hp_kua = cursorlocal.fetchall()
    jumrow_hp_kua = cursorlocal.rowcount
    print(no_wa)
    print(jumrow_hp_kua)
    if jumrow_hp_kua > 0:
        pecah_ac = pesan2.split("/", 3)
        no_ac = pecah_ac[0]
        ac = pecah_ac[1].upper()
        thn_ac = pecah_ac[2]
        no_ac_lengkap = no_ac + "/" + ac + "/" + thn_ac + "/" + kodePa

        koneksipp = koneksisipp()
        cursorcekac = koneksipp.cursor()
        sql_cek_ac = "SELECT A.perkara_id, A.nomor_akta_cerai, A.tgl_akta_cerai, A.no_seri_akta_cerai, A.jenis_cerai, A.qobla_bada, A.perceraian_ke, A.keadaan_istri, B.tanggal_pendaftaran, B.nomor_perkara, B.pihak1_text, B.pihak2_text, C.kua_tempat_nikah, C.tgl_kutipan_akta_nikah, C.no_kutipan_akta_nikah FROM perkara_akta_cerai A, perkara B, perkara_data_pernikahan C WHERE A.perkara_id=B.perkara_id AND A.perkara_id=C.perkara_id AND A.nomor_akta_cerai=%s"
        cursorcekac.execute(sql_cek_ac, (no_ac_lengkap,))
        result_data_ac = cursorcekac.fetchall()
        jumrow_data_ac = cursorcekac.rowcount
        if jumrow_data_ac > 0:
            global dataac
            for dataac in result_data_ac:
                nomoraktacerai = dataac[1]
                tanggalac = str(dataac[2])
                nomorseriaktacerai = dataac[3]
                jeniscerai = dataac[4]
                qoblabada = dataac[5]
                perceraianke = str(dataac[6])
                keadaanistri = str(dataac[7])
                tangalpendaftaran = str(dataac[8])
                nomorperkara = dataac[9]
                namap = dataac[10]
                namat = dataac[11]
                kuatempatnikah = dataac[12]
                tanggalkutipanaktanikah = str(dataac[13])
                nomorkutipanaktanikah = dataac[14]
                # print(tglac)

                jawaban = "*VALIDASI AKTA CERAI* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "" + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Nomor Seri Akta Cerai :* " + nomorseriaktacerai + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Nomor Akta Cerai :* " + nomoraktacerai + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Nomor Perkara :* " + nomorperkara + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Jenis Cerai :* " + jeniscerai + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Nama P :* " + namap + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Nama T :* " + namat + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Perceraian ke :* " + perceraianke + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Tgl Akta Cerai :* " + tanggalac + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Kutipan Akta Nikah :* " + kuatempatnikah + " Tanggal " + tanggalkutipanaktanikah + " Nomor " + nomorkutipanaktanikah + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + " *VAKTA* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + " _Validasi Akta Cerai " + namapa + "_ \n"
                text_box.send_keys(jawaban)
                print(jawaban)

        else: #No Aktecerai tidak ada
            jawaban = "*Nomor Akta Cerai  " + no_ac_lengkap + " tidak ditemukan!*" + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Pastikan Anda menulis Nomor Akta Cerai dengan benar!*" + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*VAKTA*"  + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Validasi Akta Cerai" + namapa + "_ \n"
            #send_whatsapp_msg(no_wa, jawaban)
            text_box.send_keys(jawaban)
            print(jawaban)
            sleep(1)
    else: #No HP belum terdaftar di tabel KUA
        jawaban = "*Nomor Anda Belum Terdaftar di Sistem Kami!*" + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Silahkan hubungi Admin kami di Nomor WA 6285286444567 untuk mendaftarkan nomor anda!" + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*VAKTA*"  + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Validasi Akta Cerai" + namapa + "_ \n"
        #send_whatsapp_msg(no_wa, jawaban)
        text_box.send_keys(jawaban)
        print(jawaban)
        sleep(1)
    koneklocal.close()

def _reply_antri(name,message):
    print("antri_sidang")
    koneklocal = koneksilocal()
    if koneklocal.is_connected():
        cursorlocal = koneklocal.cursor()
        no_wa = re.sub('[^0-9]', '', name)
        jakarta = pytz.timezone("Asia/Jakarta")
        sa_time = datetime.now(jakarta)
        sqllocal_antri = "insert into " + namadatabaselocal + ".antri_sidang (no_wa,isi_pesan,tgl_input) values (%s,%s,%s)"
        cursorlocal.execute(sqllocal_antri, (no_wa, message, sa_time))
        print(no_wa)
        print(message)
        print(sa_time)
        if cursorlocal.lastrowid:
            print('last insert id antri', cursorlocal.lastrowid)
        else:
            print('last insert id not found')

    koneklocal.commit()
    koneklocal.close()

    text_box = browser.find_element_by_class_name(_TEXTBOX_)

    jawaban = "*Mohon tunggu sebentar.... sedang diproses oleh server kami...*" + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "" + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*ASIAP*" + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Antrian Sidang Via WhatsApp" + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_" + namapa + "_ \n"
    text_box.send_keys(jawaban)
    print(jawaban)
    sleep(1)

def _reply_putusan(pesan2):
    print("Reply cek Putus")
    text_box = browser.find_element_by_class_name(_TEXTBOX_)
    # pesan2_split = pesan2.split("#", 1)
    # getInfo(pesan1,pesan2)
    koneksipp = koneksisipp()
    cursor = koneksipp.cursor()
    pecah_perk = pesan2.split("/", 3)
    no_perk = pecah_perk[0]
    no_perk = no_perk.lstrip("0")
    # jns_perk = pecah_perk[1][4:].upper()
    jns_perk = pecah_perk[1].upper()
    jns_perk = jns_perk.replace("PDT.", "Pdt.")
    thn_perk = pecah_perk[2]
    no_perk_lengkap = no_perk + "/" + jns_perk + "/" + thn_perk + "/" + kodePa
    sql = "SELECT b.tanggal_putusan, case b.status_putusan_id when 62 then 'dikabulkan' when 63 then 'ditolak' when 64 then 'tidak dapat diterima' when 65 then 'digugurkan' when 66 then 'dicoret dari register' when 67 then 'dicabut' when 7 then 'dicabut' else '-' end as status_putusan,a.proses_terakhir_text as tahapan FROM perkara a left join perkara_putusan b on a.perkara_id=b.perkara_id WHERE a.perkara_id=(select perkara_id from perkara where nomor_perkara=%s)"
    cursor.execute(sql, (no_perk_lengkap,))
    resultsputusan = cursor.fetchall()
    jumrowput = cursor.rowcount
    # print(str(jumrowput))
    if jumrowput == 0:
        jawaban = "Nomor Perkara :" + nomorperkara + " tidak ditemukan di database \n"
        text_box.send_keys(jawaban)
    else:
        global dataputusan
        for dataputusan in resultsputusan:
            # print(dataputusan)
            nomorperkara = no_perk_lengkap
            tglputusan = str(dataputusan[0])
            statusputusan = dataputusan[1]
            tahapanputusan = dataputusan[2]
            if "None" in tglputusan:
                jawaban = "Perkara Nomor " + nomorperkara + " *Belum Putus* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Tahapan Perkara : *" + tahapanputusan + "* \n"
                text_box.send_keys(jawaban)
            else:
                jawaban = "*Nomor Perkara :* " + nomorperkara + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Tgl Putusan :* " + tglputusan + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Status :* " + statusputusan + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Tahapan Perkara :* " + tahapanputusan + " \n"
                text_box.send_keys(jawaban)
    koneksipp.close()


def _reply_keuangan(pesan2):
    print("reply cek Keuangan Perkara")
    text_box = browser.find_element_by_class_name(_TEXTBOX_)
    # pesan2_split = pesan2.split("#", 1)
    # getInfo(pesan1,pesan2)
    koneksipp = koneksisipp()
    cursor = koneksipp.cursor()
    pecah_perk = pesan2.split("/", 3)
    no_perk = pecah_perk[0]
    no_perk = no_perk.lstrip("0")
    # jns_perk = pecah_perk[1][4:].upper()
    jns_perk = pecah_perk[1].upper()
    jns_perk = jns_perk.replace("PDT.", "Pdt.")
    thn_perk = pecah_perk[2]
    no_perk_lengkap = no_perk + "/" + jns_perk + "/" + thn_perk + "/" + kodePa
    sql = "SELECT SUM(CASE WHEN tahapan_id=10 AND jenis_transaksi=1 AND (pihak_ke=1 OR pihak_ke IS NULL)THEN jumlah ELSE 0 END) AS total_panjar,SUM(CASE WHEN tahapan_id=10 AND jenis_transaksi=-1 AND (pihak_ke=1 OR pihak_ke IS NULL) THEN jumlah ELSE 0 END) AS total_pengeluaran, SUM(CASE WHEN tahapan_id=10 AND jenis_transaksi=1 AND (pihak_ke=1 OR pihak_ke IS NULL) THEN jumlah ELSE 0 END)-SUM(CASE WHEN tahapan_id=10 AND jenis_transaksi=-1 AND (pihak_ke=1 OR pihak_ke IS NULL) THEN jumlah ELSE 0 END) AS sisa FROM perkara_biaya WHERE perkara_id=(select perkara_id from perkara where nomor_perkara=%s)"
    cursor.execute(sql, (no_perk_lengkap,))
    resultskeuangan = cursor.fetchall()
    jumrowkeu = cursor.rowcount
    # print(str(jumrowkeu))
    if jumrowkeu == 0:
        jawaban = "Data Keuangan Perkara dengan Nomor Perkara :*" + nomorperkara + "* tidak ditemukan di database \n"
        text_box.send_keys(jawaban)
    else:
        global datakeuangan
        for datakeuangan in resultskeuangan:
            locale.setlocale(locale.LC_NUMERIC, '')
            nomorperkara = no_perk_lengkap
            total_panjar = str(datakeuangan[0])
            # print(number_format(int(float(total_panjar)),2))
            if "None" in total_panjar:
                jawaban = "Data Keuangan Perkara dengan Nomor Perkara : *" + nomorperkara + "* tidak ditemukan \n"
                text_box.send_keys(jawaban)
            else:
                totalpanjar = float(total_panjar)
                total_pengeluaran = str(datakeuangan[1])
                sisa = str(datakeuangan[2])
                jawaban = "*Nomor Perkara :* " + nomorperkara + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Total Panjar :* Rp." + number_format(
                    int(totalpanjar),
                    2) + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Total Pengeluaran :* Rp." + number_format(
                    int(float(total_pengeluaran)),
                    2) + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Sisa Panjar Perkara :* Rp." + number_format(
                    int(float(sisa)), 2) + " \n"
                text_box.send_keys(jawaban)
    koneksipp.close()



def chat_history():
    text_bubbles = browser.find_elements_by_class_name("message-in")  # message-in = receiver, message-out = sender
    tmp_queue = []
    try:
        for bubble_ijo in text_bubbles:
            msg_texts = bubble_ijo.find_elements_by_class_name("copyable-text")
            for msg in msg_texts:
                tmp_queue.append(msg.text.lower())

        if len(tmp_queue) > 0:
            return tmp_queue[-1]  # Tampung pesan masuk ke antrian tmp_queue

    except StaleElementReferenceException as e:
        print(str(e))
        pass

def cari_wa_baru():
    try:
        unread = browser.find_elements_by_class_name(_UNREAD_)  # balon hjau memberitahukan ada pesan baru _2zCfw
        name, message = '', ''
        if len(unread) > 0:
            # print("pesan lebih dari 2 = "+str(unread))
            ele = unread[-1]
            action = webdriver.common.action_chains.ActionChains(browser)
            action.move_to_element_with_offset(ele, 0, -20)  # geser kekiri dari titik hijau

            # di klik 2 kali karena kadang kadang whatsapp web gak respon kalau nggak 2 kali
            try:
                action.click()
                action.perform()
                action.click()
                action.perform()
            except Exception as e:
                pass

            try:
                name = browser.find_element_by_class_name(_NAMAKONTAK_).text  # Contactname _6xQdq
                if name == "WARGA_PA_MALANG":
                    pass
                    names = [namaakunparkircursor]  # akun parkir untuk cursor setelah eksekusi pesan
                    for name in names:
                        person = browser.find_element_by_xpath('//span[@title = "{}"]'.format(name))
                        person.click()
                else:
                    message = chat_history()  # isi pesan di tampungan tmp_queue
                    nomorhppihak = re.sub('[^0-9]', '', name)
                    nomorhppihakfull = nomorhppihak.replace('62', '0', 2)
                    no_hp = nomorhppihak.replace('62', '0', 2)
                    print(message)
                    # simpan pesan masuk kedalam database lokal
                    if message == "":
                        text_box = browser.find_element_by_class_name(_TEXTBOX_)
                        response = "Maaf! *" + _NAMASINGKATANAPLIKASI_ + "* hanya bisa mengenali pesan text saja. *" + _NAMASINGKATANAPLIKASI_ + "* hanya bisa menjawab pesan yang sesuai dengan kata kunci saja. Untuk melihat kata kunci yang tersedia silahkan ketik *INFO*\n"
                        text_box.send_keys(response)

                        names = [namaakunparkircursor]  # akun parkir untuk cursor setelah eksekusi pesan
                        for name in names:
                            person = browser.find_element_by_xpath('//span[@title = "{}"]'.format(name))
                            person.click()

                    else:
                        koneklocal = koneksilocal()
                        if koneklocal.is_connected():
                            cursorlocal = koneklocal.cursor()
                            no_wa = re.sub('[^0-9]', '', name)
                            jakarta = pytz.timezone("Asia/Jakarta")
                            sa_time = datetime.now(jakarta)
                            sqllocal = "insert into inbox(no_wa,isi_pesan,tgl_input) values (%s,%s,%s)"
                            cursorlocal.execute(sqllocal, (no_wa, message, sa_time))
                            print(no_wa)
                            print(nomorhppihakfull)
                            if cursorlocal.lastrowid:
                                print('last insert id cek wa masuk', cursorlocal.lastrowid)
                            else:
                                print('last insert id not found')

                        koneklocal.commit()
                        koneklocal.close()

                        pesan = message.split("#")
                        print(len(pesan))
                        if len(pesan) == 1:
                            text_box = browser.find_element_by_class_name(_TEXTBOX_)
                            pesan1 = pesan[0].lower()
                            koneklocal = koneksilocal()
                            cursorlocal = koneklocal.cursor()
                            querykatakunci = "select * from kata_kunci where kata_kunci=%s"
                            cursorlocal.execute(querykatakunci, (pesan1,))
                            results = cursorlocal.fetchall()

                            row = cursorlocal.rowcount
                            if row >= 1:
                                global katakunciumum
                                for katakunciumum in results:
                                    ganti = katakunciumum[2].replace("|", "~")
                                    for part in ganti.split('~'):
                                        action = webdriver.common.action_chains.ActionChains(browser)
                                        text_box.send_keys(part)
                                        action.key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).perform()
                                text_box.send_keys(" \n")
                                koneklocal.commit()
                                koneklocal.close()
                            else:
                                text_box = browser.find_element_by_class_name(_TEXTBOX_)
                                response = "Kata Kunci tidak dikenali, untuk mulai menggunakan layanan " + _NAMASINGKATANAPLIKASI_ + " kirim pesan dengan kata kunci *INFO* \n"
                                text_box.send_keys(response)

                        elif len(pesan) == 2:
                            pesan1 = pesan[0].lower()
                            pesan2 = pesan[1].lower()
                            text_box = browser.find_element_by_class_name(_TEXTBOX_)
                            if 'info' in pesan1:
                                koneksipp = koneksisipp()
                                cursor = koneksipp.cursor()
                                pecah_perk = pesan2.split("/", 3)
                                no_perk = pecah_perk[0]
                                no_perk = no_perk.lstrip("0")
                                # jns_perk = pecah_perk[1][4:].upper()
                                jns_perk = pecah_perk[1].upper()
                                jns_perk = jns_perk.replace("PDT.", "Pdt.")
                                thn_perk = pecah_perk[2]
                                no_perk_lengkap = no_perk + "/" + jns_perk + "/" + thn_perk + "/" + kodePa
                                sql = "select perkara_id,nomor_perkara,pihak1_text,pihak2_text,para_pihak,alur_perkara_id,tanggal_pendaftaran,jenis_perkara_id,jenis_perkara_nama,tahapan_terakhir_text,proses_terakhir_text from perkara where nomor_perkara =%s"
                                cursor.execute(sql, (no_perk_lengkap,))
                                results = cursor.fetchall()
                                jumrowperkara = cursor.rowcount
                                print(str(jumrowperkara))
                                if jumrowperkara == 1:
                                    global data
                                    for data in results:
                                        # print(data)
                                        nomorperkara = data[1]
                                        cursorphone = koneksipp.cursor()
                                        sqltelepon = "select telepon from pihak where telepon=%s"
                                        cursorphone.execute(sqltelepon, (nomorhppihakfull,))
                                        hasilphone = cursorphone.fetchall()
                                        jumphone = cursorphone.rowcount
                                        if "0" in str(jumphone):
                                            namap = "_Disamarkan_"
                                            namat = "_Disamarkan_"
                                        else:
                                            namap = data[2]
                                            namat = data[3]
                                        tgldaftar = str(data[6])
                                        namajnsperk = data[8]
                                        tahapan_terakhir_text = data[9]
                                        proses_terakhir = data[10]
                                        jawaban = "*Nomor Perkara :* " + nomorperkara + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Nama P :* " + namap + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Nama T :* " + namat + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Tgl Daftar :* " + tgldaftar + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Jenis Perkara :* " + namajnsperk + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Tahapan Perkara:* " + tahapan_terakhir_text + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Proses Perkara :* " + proses_terakhir + " \n"
                                        text_box.send_keys(jawaban)
                                        koneksipp.close()
                                else:
                                    jawaban = "Nomor Perkara : *" + no_perk_lengkap + "* tidak ditemukan, pastikan Anda memasukan nomor perkara dengan benar." + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Format penulisan yang benar adalah *info#nomorperkara*" + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Contoh Nomor Perkara : *123/Pdt.G/2020/PA.MLG* menjadi *info#123/Pdt.G/2020/PA.MLG* \n"
                                    text_box.send_keys(jawaban)
                                    koneksipp.close()


                            elif 'sidang' in pesan1:

                                _reply_sidang(pesan2)

                            elif 'vakta' in pesan1:

                                _reply_vakta(pesan2,no_hp,no_wa)

                            elif 'akta' in pesan1:

                                _reply_akta(pesan2, nomorhppihakfull)

                            elif 'putusan' in pesan1:

                                _reply_putusan(pesan2)


                            elif 'keuangan' in pesan1:

                                _reply_keuangan(pesan2)

                            elif 'antri' in pesan1:

                                _reply_antri(name,message)

                            else:

                                text_box = browser.find_element_by_class_name(_TEXTBOX_)

                                response = "Kata Kunci tidak dikenali, untuk mulai menggunakan layanan " + _NAMASINGKATANAPLIKASI_ + " kirim pesan dengan kata kunci *INFO* \n"

                                text_box.send_keys(response)

                        elif len(pesan) > 3:
                            print("Cek Panjar Biaya Perkara")
                            locale.setlocale(locale.LC_NUMERIC, '')
                            pesan1 = pesan[0].lower().replace(" ", "").title()
                            pesan2 = pesan[1].lower().replace(" ", "").title()
                            pesan3 = pesan[2].lower().replace(" ", "").title()
                            pesan4 = pesan[3].lower().replace(" ", "").title()
                            jenis_perk_gugat = ['Cg', 'Paw', 'Aua', 'Diska', 'Haa', 'Isbat', 'Poligami']
                            jenis_perk_talak = ['Ct']
                            if (pesan1 == "Panjar" or pesan1 == "Biaya"):
                                print("jika panjar atau biaya")
                                if pesan3:
                                    koneklocal = koneksilocal()
                                    cursorlocal = koneklocal.cursor()
                                    sqllocal = "select kecamatan,nilai from radius where kecamatan=%s limit 1"
                                    cursorlocal.execute(sqllocal, (pesan3,))
                                    resultspesan3 = cursorlocal.fetchall()
                                    global pglp
                                    for pglp in resultspesan3:
                                        nilai_biayap = pglp[1]
                                    koneklocal.commit()
                                    koneklocal.close()
                                if pesan4:
                                    koneklocal = koneksilocal()
                                    cursorlocal = koneklocal.cursor()
                                    sqllocal = "select kecamatan,nilai from radius where kecamatan=%s limit 1"
                                    cursorlocal.execute(sqllocal, (pesan4,))
                                    resultspesan4 = cursorlocal.fetchall()
                                    global pglt
                                    for pglt in resultspesan4:
                                        nilai_biayat = pglt[1]
                                    koneklocal.commit()
                                    koneklocal.close()

                                koneklocal = koneksilocal()
                                cursorlocal = koneklocal.cursor()
                                sqllocal = "select SUM(biaya) as jumlahkompbiaya from komponen_biaya where status ='aktif' "
                                cursorlocal.execute(sqllocal)
                                resultskompbiaya = cursorlocal.fetchall()
                                global komponenbiaya
                                for komponenbiaya in resultskompbiaya:
                                    nilai_komponen_biaya = komponenbiaya[0]
                                    print("nilai_komponen_biaya")
                                    print(nilai_komponen_biaya)
                                koneklocal.commit()
                                koneklocal.close()

                                text_box = browser.find_element_by_class_name(_TEXTBOX_)
                                if str(pesan2) in jenis_perk_gugat:
                                    total_biaya = (nilai_biayap * _PERKALIAN_BIAYA_P_) + (
                                            nilai_biayat * _PERKALIAN_BIAYA_T_) + nilai_komponen_biaya
                                else:
                                    total_biaya = (nilai_biayap * 4) + (
                                            nilai_biayat * 5) + nilai_komponen_biaya
                                print("total_biaya")
                                print(total_biaya)
                                response = "Perkiraan Panjar Biaya yang harus dipersiapkan adalah : *Rp." + number_format(
                                    int(float(total_biaya)),
                                    2) + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*PERHATIAN!* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Perhitungan Panjar ini bersifat  Perkiraan, bisa berubah sewaktu waktu, untuk total panjar yang benar ditentukan saat anda melakukan Pendaftaran Perkara di kantor Pengadilan Agama Kabupaten Malang_ \n"
                                text_box.send_keys(response)
                            else:
                                pass
                        else:
                            text_box = browser.find_element_by_class_name(_TEXTBOX_)
                            response = "Maaf! *" + _NAMASINGKATANAPLIKASI_ + "* tidak bisa menjawab pesan Anda. *" + _NAMASINGKATANAPLIKASI_ + "* hanya bisa menjawab pesan yang sesuai dengan kata kunci saja. Untuk melihat kata kunci yang tersedia silahkan ketik *INFO*\n"
                            text_box.send_keys(response)

                        sleep(2)  # tunda 1 detik untuk memarkir Kursor
                        names = [namaakunparkircursor]  # akun parkir untuk cursor setelah eksekusi pesan
                        for name in names:
                            person = browser.find_element_by_xpath('//span[@title = "{}"]'.format(name))
                            person.click()

            except Exception as e:
                print(e)
                pass

        sleep(2)  # 3 detik sleep agar tidak terlalu cepat

    except StaleElementReferenceException as e:
        print(str(e))
        pass

while True:
    # FUNGSI NOTiFIKASI WHATSAPP UNTUK INFO PERKARA
    # cari_wa_baru()
    cek_notif_outbox()
    cek_notif_outbox_group()
