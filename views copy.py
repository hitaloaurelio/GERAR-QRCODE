

from typing import Text
from django import forms
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.forms.forms import Form
from django.forms.widgets import HiddenInput, Textarea
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.list import ListView

from vaquejada.forms import RodizioForms, UpdateFormClassificadas, UpdateFormFinal, UpdateFormRodizio, UpdateFormRodizioLocucao
from .models import Rodizio, SenhaClassificada, SenhaPerdidas, Vaqueiro, Parque
from .admin import ParqueAdmin, VaqueiroAdmin
from django.db import IntegrityError
from django.forms.models import inlineformset_factory
from django.forms import formsets, modelformset_factory
# from django.shortcuts import render_to_response
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.

# from django.views.generic import ListView
# from vaquejada.models import Vaqueiro
from .models import Vaqueiro,Rodizio
from django.contrib import messages
from django.contrib.messages import constants
import qrcode


import warnings
warnings.filterwarnings("ignore")
import sys  
from PIL import Image, ImageDraw
import os
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.moduledrawers import CircleModuleDrawer

def QRCODE(request):

    url = "https://www.example.com"
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#2C585D", back_color="white")


    # Carregue a imagem da logo

    path = os.path.dirname(__file__)
    my_file = path+'\\teste2.png'
    #my_file = path+'\\image.png'
    
    Logo_link = 'logoXoce.jpg'

    logo = Image.open(my_file)

# taking base width
    basewidth = 100

# adjust image size
    wpercent = (basewidth/float(logo.size[0]))
    hsize = int((float(logo.size[1])*float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
    QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=10, border=3)

# taking url or text
    url = 'https://api.whatsapp.com/send?phone=5599981552048'

# adding URL or text to QRcode
    QRcode.add_data(url)

# generating QR code

    #QRcode.make()
    
# taking color name from user
    QRcolor = '#2C585D'

# adding color to QR code
    #QRimg = QRcode.make_image(fill_color=QRcolor, back_color="white").convert('RGBA')

    QRimg = QRcode.make_image(image_factory=StyledPilImage, module_drawer=CircleModuleDrawer()).convert('RGBA')
    #QRimg = QRcode.make_image(image_factory=StyledPilImage, fill_color=QRcolor,color_mask=RadialGradiantColorMask()).convert('RGBA')
# set size of QR code
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
	    (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)

# save the QR code generated
    #QRimg.save('Xoce_QR.png')

    print('QR code generated!')

    response = HttpResponse(content_type="image/png")
    QRimg.save(response, "PNG")
    return response




def QRCODE2(request):

    def style_eyes(img):
        img_size = img.size[0]
        eye_size = 70 #default
        quiet_zone = 40 #default
        mask = Image.new('RGBA', img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rectangle((40, 40, 110, 110), fill=255)
        draw.rectangle((img_size-110, 40, img_size-40, 110), fill=255)
        draw.rectangle((40, img_size-110, 110, img_size-40), fill=255)
        return mask

    YOUR_TEXT_OR_URL = 'https://api.whatsapp.com/send?phone=5599981552048' #hitalo
    YOUR_TEXT_OR_URL = 'https://api.whatsapp.com/send?phone=559898133-6863'#jak
    YOUR_TEXT_OR_URL = 'Telefone: (98) 3304-0442'#neres e will
    YOUR_TEXT_OR_URL = 'https://api.whatsapp.com/send?phone=559884244794'#wallace
    YOUR_TEXT_OR_URL = 'https://api.whatsapp.com/send?phone=559899158-5170'#neres 
    
    logosize = 90


    infile = sys.argv[-1]


# convert RGB to HEX function
    def rgb_to_hex(rgb):
        return '#'+'%02x%02x%02x' % rgb

# get filename
    filename = infile.split('.')[0]
# read image


    path = os.path.dirname(__file__)
    my_file = path+'\\teste3.png'
    
    
    

    logo = Image.open(my_file)
    
# convert to RGB mode
    logo_rgb = logo.convert("RGB")
# getting the RGB color from 10x10 pixel
    rgb = logo_rgb.getpixel((10,10))
# set size of the logo
    basewidth = logosize
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1])*float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)

    
    qr_big = qrcode.QRCode(error_correction = qrcode.constants.ERROR_CORRECT_H,box_size=8, border=1)
    qr_big.add_data(YOUR_TEXT_OR_URL)
    qr_big.make()

    
# Using the same color of the image automatically
# OR type color code as 'black'  or #0b4e39 
   
    


    img_qr_big = qr_big.make_image(
        fill_color='#2C585D', 
        back_color="white",
        image_factory=StyledPilImage, 
        module_drawer=CircleModuleDrawer(),
        eye_drawer=RoundedModuleDrawer(radius_ratio=1.0),
        color_mask=SolidFillColorMask(back_color=(255, 255, 255),
        front_color=(44, 88, 93)),
        ).convert('RGBA')


    pos = (
        (img_qr_big.size[0] - logo.size[0]) // 2,
        (img_qr_big.size[1] - logo.size[1]) // 2
    )

    tt = style_eyes(logo)
    img_qr_big.paste(logo, pos)

# Create final_QR directory
    try:
        os.mkdir("final_QR")
    except:
        print("folder exists")
    
#save as filenameQR.png format    
    #img_qr_big.save("final_QR/"+filename+'QR'+'.png')


    response = HttpResponse(content_type="image/png")
    img_qr_big.save(response, "PNG")
    return response
    