from django.db.models import TextChoices, IntegerChoices


class Genders(IntegerChoices):
    UNKNOWN = 0, 'Unknown'
    MALE = 1,'Male'
    FEMALE = 2, 'Female'
    NA = 9, 'Not applicable'


class Modality(TextChoices):
    vary = 'vary', 'Varying modalities'
    CR = 'CR','Computed Radiography'
    CT = 'CT','Computed Tomography'
    MR = 'MR','Magnetic Resonance'
    US = 'US','Ultrasound'
    BI = 'BT','Biomagnetic imaging'
    CD = 'CD','Color flow Doppler'
    DD = 'DD','Duplex Doppler'
    DG = 'DG','Diaphanography'
    ES = 'ES','Endoscopy'
    LS = 'LS','Laser surface scan'
    PT = 'PT','Positron emission tomography (PET)'
    RG = 'RG','Radiographic imaging (conventional film/screen)'
    ST = 'ST','Single-photon emission computed tomography (SPECT)'
    TG = 'TG','Thermography'
    XA = 'XA','X-Ray Angiography'
    RF = 'RF', 'Radio Fluoroscopy'
    RTIMAGE = 'RTIMAGE', 'Radiotherapy Image'
    RTDOSE = 'RTDOSE', 'Radiotherapy Dose'
    RTSTRUCT = 'RTSTRUCT', 'Radiotherapy Structure Set'
    RTPLAN = 'RTPLAN','Radiotherapy Plan'
    RTRECORD = 'RTRECORD', 'RT Treatment Record'
    HC = 'HC', 'Hard Copy'
    DX = 'DX','Digital Radiography'
    NM	= 'NM', 'Nuclear Medicine'
    MG = 'MG', 'Mammography'
    IO = 'IO', 'Intra-oral Radiography'
    PX = 'PX','Panoramic X-Ray'
    GM = 'GM', 'General Microscopy'
    SM = 'SM', 'Slide Microscopy'
    XC = 'XC', 'External-camera Photography'
    PR = 'PR', 'Presentation State'
    AU = 'AU', 'Audio ECG'
    EPS = 'EPS', 'ccrdiac Electrophysiology'
    HD = 'HD', 'Hemodynamic Waveform'
    SR = 'SR', 'SR Document'
    IVUS = 'IVUS', 'Intravascular Ultrasound'
    OP = 'OP', 'Ophthalmic Photography'
    SMR	= 'SMR', 'Stereometric Relationship'
    OT = 'OT','Other'
    