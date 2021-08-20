from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException, TimeoutException, InvalidSessionIdException
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from datetime import datetime
import json
import logging
import sys


# Ini untuk dijalankan paralel per propinsi
# Parameternya adalah nama propinsi di website KPU, yaitu:
# 'ACEH', 'SUMATERA UTARA', 'SUMATERA BARAT', 'RIAU', 'JAMBI', 
# 'SUMATERA SELATAN', 'BENGKULU', 'LAMPUNG', 'KEPULAUAN BANGKA BELITUNG', 
# 'KEPULAUAN RIAU', 'DKI JAKARTA', 'JAWA BARAT', 'JAWA TENGAH', 
# 'DAERAH ISTIMEWA YOGYAKARTA', 'JAWA TIMUR', 'BANTEN', 'BALI', 
# 'NUSA TENGGARA BARAT', 'NUSA TENGGARA TIMUR', 'KALIMANTAN BARAT', 
# 'KALIMANTAN TENGAH', 'KALIMANTAN SELATAN', 'KALIMANTAN TIMUR', 
# 'SULAWESI UTARA', 'SULAWESI TENGAH', 'SULAWESI SELATAN', 'SULAWESI TENGGARA', 
# 'GORONTALO', 'SULAWESI BARAT', 'MALUKU', 'MALUKU UTARA', 'PAPUA', 
# 'PAPUA BARAT', 'KALIMANTAN UTARA', 'Luar Negeri'

if len(sys.argv) > 1:
    nama_propinsi = sys.argv[1]
    file1 = nama_propinsi.lower().replace(' ', '_')
    log1 = file1 + '.log'
    logging.basicConfig(filename=log1, format='%(asctime)s %(message)s')
    json1 = file1 + '.json'
    while True:
        try:
            driver = webdriver.Chrome()
            #driver=webdriver.Firefox()
            #navigate to the url
            driver.get("https://pemilu2019.kpu.go.id/#/dprdkab/hitung-suara/")
            sleep(1)
            # WILAYAH
            wilayah = WebDriverWait(driver, 10).until(
                        expected_conditions.visibility_of_element_located((By.XPATH, '//div[@id="scope-options"]/div/div/input'))
                        )
            wilayah.send_keys("WILAYAH\n")
            # driver.find_element_by_xpath('//div[@id="scope-options"]/div/div/input').send_keys("WILAYAH\n")
            sleep(1)

            # Propinsi
            propinsi = WebDriverWait(driver, 10).until(
                        expected_conditions.visibility_of_element_located((By.XPATH, '//div[@class="form-group col-md-3"][4]/div/div/div/input'))
                        )
            try:
                propinsi.click()
            except ElementClickInterceptedException:
                sleep(5)
                propinsi = WebDriverWait(driver, 20).until(
                        expected_conditions.element_to_be_clickable((By.XPATH, '//div[@class="form-group col-md-3"][4]/div/div/div/input'))
                        )
                propinsi.click()
            sleep(1)
            
            pass_kota = False
            pass_camat = False
            pass_desa = False
            pass_tps = False
            try:
                with open(json1) as f1:
                    akhir = json.load(f1)
            except FileNotFoundError:
                akhir = {}
            if not akhir.get('propinsi'):
                akhir['propinsi'] = nama_propinsi
            
            # create csv
            nama_file = nama_propinsi.upper().replace(' ', '_') + datetime.now().strftime("_%Y_%m_%d_%H_%M_%S") + '.csv'
            f = open(nama_file, 'w')
            writer = csv.writer(f)
            row = ['PROPINSI', 'KOTA', 'CAMAT', 'DESA', 'TPS', 'DPT', 'PENGGUNA', 'PKB', 'Gerindra','PDIP','Golkar','NasDem','Garuda','Berkarya','PKS','Perindo','PPP','PSI','PAN','Hanura','Demokrat','PA','SIRA','PD Aceh','PNA','PBB','PKPI', 'SAH', 'TAK SAH', 'JUMLAH']
            writer.writerow(row)

            propinsi.send_keys(nama_propinsi + "\n")
            sleep(1)

            # Kota
            kota = WebDriverWait(driver, 10).until(
                    expected_conditions.visibility_of_element_located((By.XPATH, '//div[@class="form-group col-md-3"][5]/div/div/div/input'))
                    )
            try:
                kota.click()
            except ElementClickInterceptedException:
                sleep(5)
                kota = WebDriverWait(driver, 10).until(
                        expected_conditions.element_to_be_clickable((By.XPATH, '//div[@class="form-group col-md-3"][5]/div/div/div/input'))
                        )
                kota.click()
            sleep(1)
            i = 1
            daftar_kota = []
            while True:
                tag = '//div[@class="form-group col-md-3"][5]/div/ul/li[' + str(i) + ']'
                try:
                    # Ini gagal!
                    # pilihan = WebDriverWait(driver, 10).until(
                    #           expected_conditions.visibility_of_element_located((By.XPATH, tag))
                    #           )
                    pilihan = driver.find_element_by_xpath(tag)
                    daftar_kota.append(pilihan.text)
                    i += 1
                except NoSuchElementException:
                    break
            for nama_kota in daftar_kota:
                if not akhir.get('kota'):
                    akhir['kota'] = nama_kota
                    pass_kota = True
                # skip kota yang sudah dicatat
                if pass_kota or (nama_propinsi == akhir['propinsi'] and nama_kota == akhir['kota']):
                    pass_kota = True
                else:
                    continue
                kota.send_keys(nama_kota + "\n")
                kota_terpilih = driver.find_element_by_xpath('//div[@class="form-group col-md-3"][5]/div/div/div/span[@class="selected-tag"]')
                if kota_terpilih.text != nama_kota:
                    kota.clear
                    kota.send_keys(nama_kota)
                    i = 2
                    ketemu = False
                    while not ketemu:
                        tag = '//div[@class="form-group col-md-3"][5]/div/ul/li[' + str(i) + ']'
                        try:
                            kota_terpilih = driver.find_element_by_xpath(tag)
                            if kota_terpilih.text == nama_kota:
                                kota_terpilih.location_once_scrolled_into_view
                                kota_terpilih.click()
                                ketemu = True
                                break
                            i += 1
                        except NoSuchElementException:
                            logging.error('ERROR! Kota ' + nama_kota + ' tak bisa dipilih. Propinsi = ' + nama_propinsi)
                            break
                    if not ketemu:
                        continue  # skip kota ini
                # Kecamatan
                camat = WebDriverWait(driver, 10).until(
                        expected_conditions.visibility_of_element_located((By.XPATH, '//div[@class="form-group col-md-3"][6]/div/div/div/input'))
                        )
                try:
                    camat.click()
                except ElementClickInterceptedException:
                    sleep(5)
                    camat = WebDriverWait(driver, 20).until(
                            expected_conditions.element_to_be_clickable((By.XPATH, '//div[@class="form-group col-md-3"][6]/div/div/div/input'))
                            )
                    camat.click()
                sleep(1)
                i = 1
                daftar_camat = []
                while True:
                    tag = '//div[@class="form-group col-md-3"][6]/div/ul/li[' + str(i) + ']'
                    try:
                        pilihan = driver.find_element_by_xpath(tag)
                        daftar_camat.append(pilihan.text)
                        i += 1
                    except NoSuchElementException:
                        break
                for nama_camat in daftar_camat:
                    if not akhir.get('camat'):
                        akhir['camat'] = nama_camat
                        pass_camat = True
                    # skip camat yang sudah dicatat
                    if pass_camat or (nama_propinsi == akhir['propinsi'] and nama_kota == akhir['kota'] and nama_camat == akhir['camat']):
                        pass_camat = True
                    else:
                        continue
                    camat.send_keys(nama_camat + "\n")
                    # Desa
                    desa = WebDriverWait(driver, 10).until(
                            expected_conditions.visibility_of_element_located((By.XPATH, '//div[@class="form-group col-md-3"][7]/div/div/div/input'))
                            )
                    try:
                        desa.click()
                    except ElementClickInterceptedException:
                        sleep(5)
                        desa = WebDriverWait(driver, 20).until(
                                expected_conditions.element_to_be_clickable((By.XPATH, '//div[@class="form-group col-md-3"][7]/div/div/div/input'))
                                )
                        desa.click()
                    sleep(1)
                    i = 1
                    daftar_desa = []
                    while True:
                        tag = '//div[@class="form-group col-md-3"][7]/div/ul/li[' + str(i) + ']'
                        try:
                            pilihan = driver.find_element_by_xpath(tag)
                            daftar_desa.append(pilihan.text)
                            i += 1
                        except NoSuchElementException:
                            break
                    for nama_desa in daftar_desa:
                        if not akhir.get('desa'):
                            akhir['desa'] = nama_desa
                            pass_desa = True
                        # skip desa yang sudah dicatat
                        if pass_desa or (nama_propinsi == akhir['propinsi'] and nama_kota == akhir['kota'] and\
                                         nama_camat == akhir['camat'] and nama_desa == akhir['desa']):
                            pass_desa = True
                        else:
                            continue
                        try:
                            # desa.send_keys("GAMPONG\n")
                            # print(nama_desa)
                            desa.send_keys(nama_desa + "\n")
                        except ElementNotInteractableException:
                            sleep(5)
                            desa = WebDriverWait(driver, 20).until(
                                    expected_conditions.element_to_be_clickable((By.XPATH, '//div[@class="form-group col-md-3"][7]/div/div/div/input'))
                                    )
                            desa.send_keys(nama_desa + "\n")

                        sleep(1)
                        # TPS
                        try:
                            tps = WebDriverWait(driver, 10).until(
                                    expected_conditions.visibility_of_element_located((By.XPATH, '//div[@class="form-group col-md-3"][8]/div/div/div/input'))
                                    )
                            tps.click()
                        except ElementClickInterceptedException:
                            try:
                                sleep(5)
                                tps = WebDriverWait(driver, 20).until(
                                        expected_conditions.element_to_be_clickable((By.XPATH, '//div[@class="form-group col-md-3"][8]/div/div/div/input'))
                                        )
                                tps.click()
                            except ElementClickInterceptedException:
                                sleep(10)
                                tps = WebDriverWait(driver, 40).until(
                                        expected_conditions.element_to_be_clickable((By.XPATH, '//div[@class="form-group col-md-3"][8]/div/div/div/input'))
                                        )
                                tps.click()
                        except TimeoutException:
                            nama = nama_desa.split()
                            for kata in nama:
                                desa.clear()
                                desa.send_keys(kata)
                                sleep(1)
                                pilihan = driver.find_element_by_xpath('//div[@class="form-group col-md-3"][7]/div/ul/li[1]')
                                if pilihan.text == nama_desa:
                                    desa.send_keys("\n")
                                    break
                            else:
                                desa.clear()
                                desa.send_keys(kata)
                                sleep(1)
                                i = 1
                                ketemu = False
                                while not ketemu:
                                    tag = '//div[@class="form-group col-md-3"][7]/div/ul/li[' + str(i) + ']'
                                    try:
                                        desa_terpilih = driver.find_element_by_xpath(tag)
                                        if desa_terpilih.text == nama_desa:
                                            desa_terpilih.location_once_scrolled_into_view
                                            desa_terpilih.click()
                                            ketemu = True
                                            break
                                        i += 1
                                    except NoSuchElementException:
                                        logging.error('ERROR. Desa ' + nama_desa + ' tidak bisa dipilih. Propinsi = ' + nama_propinsi + ', Kota = ' + nama_kota + ', Camat = ' + nama_camat)
                                        break
                                if not ketemu:
                                    continue  # skip desa ini   
                            sleep(1)
                            try:
                                tps = WebDriverWait(driver, 10).until(
                                        expected_conditions.visibility_of_element_located((By.XPATH, '//div[@class="form-group col-md-3"][8]/div/div/div/input'))
                                        )
                                tps.click()
                            except ElementClickInterceptedException:
                                try:
                                    sleep(5)
                                    tps = WebDriverWait(driver, 20).until(
                                            expected_conditions.element_to_be_clickable((By.XPATH, '//div[@class="form-group col-md-3"][8]/div/div/div/input'))
                                            )
                                    tps.click()
                                except ElementClickInterceptedException:
                                    sleep(10)
                                    tps = WebDriverWait(driver, 40).until(
                                            expected_conditions.element_to_be_clickable((By.XPATH, '//div[@class="form-group col-md-3"][8]/div/div/div/input'))
                                            )
                                    tps.click()

                        sleep(1)
                        i = 1
                        daftar_tps = []
                        while True:
                            tag = '//div[@class="form-group col-md-3"][8]/div/ul/li[' + str(i) + ']'
                            try:
                                pilihan = driver.find_element_by_xpath(tag)
                                daftar_tps.append(pilihan.text)
                                i += 1
                            except NoSuchElementException:
                                break
                        for nama_tps in daftar_tps:
                            if not akhir.get('tps'):
                                akhir['tps'] = nama_tps
                                pass_tps = True
                            # skip tps yang sudah dicatat
                            if pass_tps or (nama_propinsi == akhir['propinsi'] and nama_kota == akhir['kota'] and\
                                            nama_camat == akhir['camat'] and nama_desa == akhir['desa'] and nama_tps == akhir['tps']):
                                if not pass_tps:
                                    pass_tps = True
                                    continue
                            else:
                                continue
                            try:
                                tps.send_keys(nama_tps + "\n")
                            except ElementNotInteractableException:
                                sleep(5)
                                WebDriverWait(driver, 20).until(
                                    expected_conditions.element_to_be_clickable((By.XPATH, '//div[@class="form-group col-md-3"][8]/div/div/div/input'))
                                    )
                                try:
                                    tps.send_keys(nama_tps + "\n")
                                except ElementNotInteractableException:
                                    sleep(10)
                                    WebDriverWait(driver, 40).until(
                                        expected_conditions.element_to_be_clickable((By.XPATH, '//div[@class="form-group col-md-3"][8]/div/div/div/input'))
                                        )
                                    tps.send_keys(nama_tps + "\n")
                            sleep(1)
                            # Save to file
                            row = [nama_propinsi, nama_kota, nama_camat, nama_desa, nama_tps]
                            # skip jika: Data Belum Tersedia
                            try:
                                tag = driver.find_element_by_xpath("//table[1]/tr[2]/td[2]")
                            except NoSuchElementException:
                                sleep(5)
                                try:
                                    tag = WebDriverWait(driver, 10).until(
                                            expected_conditions.presence_of_element_located((By.XPATH, "//table[1]/tr[2]/td[2]"))
                                            )
                                except TimeoutException:
                                    row.extend(['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'])
                                    writer.writerow(row)
                                    f.flush()
                                    akhir = {
                                        'propinsi': nama_propinsi,
                                        'kota': nama_kota,
                                        'camat': nama_camat,
                                        'desa': nama_desa,
                                        'tps': nama_tps
                                    }
                                    with open(json1, 'w') as f2:
                                        json.dump(akhir, f2)
                                    continue
                            # DPT
                            for i in range(2,4):
                                try:
                                    tag = driver.find_element_by_xpath("//table[1]/tr[" + str(i) + "]/td[2]")
                                except NoSuchElementException:
                                    sleep(5)
                                    tag = WebDriverWait(driver, 20).until(
                                            expected_conditions.presence_of_element_located((By.XPATH, "//table[1]/tr[" + str(i) + "]/td[2]"))
                                            )    
                                row.append(tag.text)
                            # Partai
                            if nama_propinsi == 'ACEH':
                                for i in range(2,22):
                                    try:
                                        tag = driver.find_element_by_xpath("//table[2]/tr[" + str(i) + "]/td[3]")
                                    except NoSuchElementException:
                                        sleep(5)
                                        tag = WebDriverWait(driver, 20).until(
                                                expected_conditions.presence_of_element_located((By.XPATH, "//table[2]/tr[" + str(i) + "]/td[3]"))
                                                )
                                    row.append(tag.text)
                            else:
                                for i in range(2,18):
                                    try:
                                        tag = driver.find_element_by_xpath("//table[2]/tr[" + str(i) + "]/td[3]")
                                    except NoSuchElementException:
                                        sleep(5)
                                        tag = WebDriverWait(driver, 20).until(
                                                expected_conditions.presence_of_element_located((By.XPATH, "//table[2]/tr[" + str(i) + "]/td[3]"))
                                                )
                                    if i == 16:
                                        row.extend(['0','0','0','0'])
                                    row.append(tag.text)
                            # Suara sah
                            for i in range(2,5):
                                try:
                                    tag = driver.find_element_by_xpath("//table[3]/tr[" + str(i) + "]/td[3]")
                                except NoSuchElementException:
                                    sleep(5)
                                    tag = WebDriverWait(driver, 10).until(
                                            expected_conditions.presence_of_element_located((By.XPATH, "//table[3]/tr[" + str(i) + "]/td[3]"))
                                            )
                                row.append(tag.text)
                            writer.writerow(row)
                            # tulis buffer csv ke file
                            f.flush()
                            akhir = {
                                'propinsi': nama_propinsi,
                                'kota': nama_kota,
                                'camat': nama_camat,
                                'desa': nama_desa,
                                'tps': nama_tps
                            }
                            with open(json1, 'w') as f2:
                                json.dump(akhir, f2)
            # close csv
            f.close()
            logging.info('FINISH')
            driver.close()
            sys.exit(0)
        except Exception:
            logging.exception('ERROR')
        finally:
            try:
                f.close()
            except Exception:
                logging.exception('ERROR')
            # close the browser
            try:
                driver.close()
            except Exception:
                logging.exception('ERROR')
    logging.info('CLOSE')
