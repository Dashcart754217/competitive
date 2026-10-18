import os
import sys

# Ensure local module directory has highest priority in sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import logging
from database import get_connection

logger = logging.getLogger(__name__)

SEED_QUESTIONS = [
    # ==========================
    # 🧬 BIOLOGY (ENGLISH, HINDI, ODIA, HINGLISH)
    # ==========================
    {
        "subject": "biology", "topic": "bio_cell", "exam_level": "neet", "language": "en",
        "question_text": "Which organelle is known as the 'Powerhouse of the Cell' and possesses its own DNA and 70S ribosomes?",
        "opt_a": "Golgi Apparatus", "opt_b": "Mitochondria", "opt_c": "Endoplasmic Reticulum", "opt_d": "Lysosome",
        "correct_opt": "B",
        "explanation": "Mitochondria generate most of the cell's ATP via aerobic cellular respiration and are semi-autonomous organelles having circular dsDNA and 70S ribosomes.",
        "hint": "Think of the organelle where Krebs cycle and ATP synthesis occur."
    },
    {
        "subject": "biology", "topic": "bio_cell", "exam_level": "neet", "language": "hi",
        "question_text": "कोशिका का 'शक्तिगृह' (Powerhouse of the cell) किसे कहा जाता है, जिसके पास अपना DNA और 70S राइबोसोम होता है?",
        "opt_a": "गॉल्जी काय", "opt_b": "माइटोकॉन्ड्रिया", "opt_c": "लाइसोसोम", "opt_d": "राइबोसोम",
        "correct_opt": "B",
        "explanation": "माइटोकॉन्ड्रिया कोशिकीय श्वसन द्वारा ATP का निर्माण करता है और इसके पास अपना वृत्ताकार DNA तथा 70S राइबोसोम मौजूद होता है।",
        "hint": "यह अंगक क्रेब्स चक्र (Krebs Cycle) के लिए उत्तरदायी है।"
    },
    {
        "subject": "biology", "topic": "bio_cell", "exam_level": "osssc", "language": "or",
        "question_text": "କେଉଁ କୋଷାଙ୍ଗକୁ 'କୋଷର ଶକ୍ତିକେନ୍ଦ୍ର' (Powerhouse of the cell) କୁହାଯାଏ?",
        "opt_a": "ଲାଇସୋଜୋମ୍", "opt_b": "ମାଇଟୋକଣ୍ଡ୍ରିଆ", "opt_c": "ଗଲଗିପିଣ୍ଡ", "opt_d": "ରାଇବୋଜୋମ୍",
        "correct_opt": "B",
        "explanation": "ମାଇଟୋକଣ୍ଡ୍ରିଆରେ ଶ୍ୱାସକ୍ରିୟା ଦ୍ୱାରା ATP ଆକାରରେ ଶକ୍ତି ଉତ୍ପନ୍ନ ହୋଇ ସଞ୍ଚିତ ହୋଇ ରହିଥାଏ, ତେଣୁ ଏହାକୁ କୋଷର ଶକ୍ତିକେନ୍ଦ୍ର କୁହାଯାଏ।",
        "hint": "ଏହି କୋଷାଙ୍ଗ ATP ଉତ୍ପାଦନ କରେ।"
    },
    {
        "subject": "biology", "topic": "bio_cell", "exam_level": "neet", "language": "hinglish",
        "question_text": "Cell ka 'Powerhouse' kis organelle ko kaha jata hai jisme khud ka circular DNA aur 70S ribosomes hota hai?",
        "opt_a": "Golgi body", "opt_b": "Mitochondria", "opt_c": "Lysosome", "opt_d": "Centrosome",
        "correct_opt": "B",
        "explanation": "Mitochondria cellular respiration ke through ATP generate karta hai aur ye semi-autonomous organelle hota hai.",
        "hint": "Krebs cycle iske matrix mein chalti hai."
    },
    {
        "subject": "biology", "topic": "bio_genetics", "exam_level": "neet", "language": "en",
        "question_text": "According to Mendel's Dihybrid Cross, what is the expected phenotypic ratio in the F2 generation?",
        "opt_a": "3:1", "opt_b": "9:3:3:1", "opt_c": "1:2:1", "opt_d": "9:7",
        "correct_opt": "B",
        "explanation": "Mendel's Law of Independent Assortment produces a classic phenotypic dihybrid ratio of 9 (Round Yellow) : 3 (Round Green) : 3 (Wrinkled Yellow) : 1 (Wrinkled Green).",
        "hint": "There are 4 different phenotypes from 16 total offspring boxes."
    },
    {
        "subject": "biology", "topic": "bio_human_physio", "exam_level": "upsc", "language": "hi",
        "question_text": "मानव शरीर में इंसुलिन (Insulin) हार्मोन का स्राव किस ग्रंथि द्वारा होता है?",
        "opt_a": "थायराइड", "opt_b": "अग्न्याशय (Pancreas)", "opt_c": "पीयूष ग्रंथि", "opt_d": "यकृत (Liver)",
        "correct_opt": "B",
        "explanation": "इंसुलिन का स्राव अग्न्याशय (Pancreas) की लैंगरहेंस की द्वीपिकाओं (Islets of Langerhans) की बीटा कोशिकाओं (Beta cells) द्वारा होता है, जो रक्त में शर्करा स्तर नियंत्रित करता है।",
        "hint": "यह एक मिश्रित ग्रंथि (Mixed Gland) है जो पेट के ठीक पीछे स्थित होती है।"
    },
    {
        "subject": "biology", "topic": "bio_human_physio", "exam_level": "opsc", "language": "or",
        "question_text": "ମାନବ ଶରୀରରେ ରକ୍ତ ଜମାଟ ବାନ୍ଧିବାରେ (Blood Clotting) କେଉଁ ଭିଟାମିନ୍ ମୁଖ୍ୟ ଭୂମିକା ଗ୍ରହଣ କରେ?",
        "opt_a": "ଭିଟାମିନ୍ A", "opt_b": "ଭିଟାମିନ୍ C", "opt_c": "ଭିଟାମିନ୍ K", "opt_d": "ଭିଟାମିନ୍ D",
        "correct_opt": "C",
        "explanation": "ଭିଟାମିନ୍ K ଯକୃତରେ ପ୍ରୋଥ୍ରୋମ୍ବିନ୍ (Prothrombin) ସଂଶ୍ଳେଷଣ ପାଇଁ ଅତ୍ୟାବଶ୍ୟକ, ଯାହା ରକ୍ତ ଜମାଟ ବାନ୍ଧିବାରେ ସାହାଯ୍ୟ କରେ।",
        "hint": "ଏହାକୁ ଫାଇଲୋକୁଇନୋନ୍ (Phylloquinone) ମଧ୍ୟ କୁହାଯାଏ।"
    },

    # ==========================
    # ⚡ PHYSICS (ENGLISH, HINDI, ODIA, HINGLISH)
    # ==========================
    {
        "subject": "physics", "topic": "phy_mechanics", "exam_level": "jee_main", "language": "en",
        "question_text": "A particle moves in a circle of radius R with constant speed v. What is the magnitude of its centripetal acceleration?",
        "opt_a": "v / R", "opt_b": "v^2 / R", "opt_c": "v^2 * R", "opt_d": "Zero",
        "correct_opt": "B",
        "explanation": "In uniform circular motion, although the speed is constant, the direction continuously changes, giving a radially inward centripetal acceleration a_c = v^2 / R.",
        "hint": "Dimensions of acceleration are [L T^-2]."
    },
    {
        "subject": "physics", "topic": "phy_optics", "exam_level": "ssc", "language": "en",
        "question_text": "The optical phenomenon responsible for the sparkling of diamonds and optical fiber transmission is:",
        "opt_a": "Refraction", "opt_b": "Total Internal Reflection", "opt_c": "Interference", "opt_d": "Diffraction",
        "correct_opt": "B",
        "explanation": "Total Internal Reflection (TIR) occurs when light travels from a denser to rarer medium at an angle of incidence greater than the critical angle. Diamond's critical angle is very small (~24.4°).",
        "hint": "Light rays get trapped and reflect entirely inside the medium."
    },
    {
        "subject": "physics", "topic": "phy_mechanics", "exam_level": "ssc", "language": "hi",
        "question_text": "रॉकेट का प्रक्षेपण न्यूटन के किस गति नियम पर आधारित है?",
        "opt_a": "प्रथम नियम", "opt_b": "द्वितीय नियम", "opt_c": "तृतीय नियम (क्रिया-प्रतिक्रिया)", "opt_d": "गुरुत्वाकर्षण नियम",
        "correct_opt": "C",
        "explanation": "रॉकेट प्रक्षेपण न्यूटन के तृतीय नियम (प्रत्येक क्रिया के बराबर एवं विपरीत दिशा में प्रतिक्रिया होती है) तथा रेखीय संवेग संरक्षण के सिद्धांत पर कार्य करता है।",
        "hint": "Action-Reaction Principle याद करें।"
    },
    {
        "subject": "physics", "topic": "phy_electromag", "exam_level": "ossc", "language": "or",
        "question_text": "ବିଦ୍ୟୁତ ବିଭବାନ୍ତର (Electric Potential Difference) ର SI ଏକକ କ’ଣ?",
        "opt_a": "ଆମ୍ପିୟର (Ampere)", "opt_b": "ଭୋଲ୍ଟ (Volt)", "opt_c": "ଓମ୍ (Ohm)", "opt_d": "ଜୁଲ୍ (Joule)",
        "correct_opt": "B",
        "explanation": "ବିଦ୍ୟୁତ ବିଭବାନ୍ତରର SI ଏକକ ହେଉଛି ଭୋଲ୍ଟ (Volt), ଯାହା ଏକ କୁଲମ୍ ଚାର୍ଜ୍ ପ୍ରବାହିତ କରିବା ପାଇଁ ଏକ ଜୁଲ୍ କାର୍ଯ୍ୟକୁ ବୁଝାଏ (1 V = 1 J/C)।",
        "hint": "ଏହାର ନାମ ଆଲେସାଣ୍ଡ୍ରୋ ଭୋଲ୍ଟାଙ୍କ ନାମାନୁସାରେ ରଖାଯାଇଛି।"
    },
    {
        "subject": "physics", "topic": "phy_thermo", "exam_level": "jee_main", "language": "hinglish",
        "question_text": "Ek adiabatic process mein system aur surroundings ke beech kaun si quantity zero hoti hai?",
        "opt_a": "Work done (W)", "opt_b": "Heat exchange (dQ)", "opt_c": "Internal energy change (dU)", "opt_d": "Pressure change (dP)",
        "correct_opt": "B",
        "explanation": "Adiabatic process mein system completely insulated hota hai, isliye heat transfer dQ = 0 hota hai, aur First Law of Thermodynamics se dU = -dW.",
        "hint": "Is process me heat na toh andar aati hai na bahar jati hai."
    },

    # ==========================
    # 🧪 CHEMISTRY (ENGLISH, HINDI, ODIA, HINGLISH)
    # ==========================
    {
        "subject": "chemistry", "topic": "chem_periodic", "exam_level": "neet", "language": "en",
        "question_text": "Which element in the periodic table has the highest electronegativity according to the Pauling scale?",
        "opt_a": "Chlorine (Cl)", "opt_b": "Oxygen (O)", "opt_c": "Fluorine (F)", "opt_d": "Helium (He)",
        "correct_opt": "C",
        "explanation": "Fluorine (F) is the most electronegative element with a Pauling value of 4.0 due to its small atomic size and high nuclear attraction.",
        "hint": "It belongs to Group 17, Period 2."
    },
    {
        "subject": "chemistry", "topic": "chem_bonding", "exam_level": "11th", "language": "hi",
        "question_text": "जल के अणु (H2O) में केंद्रीय ऑक्सीजन परमाणु का संकरण (Hybridization) क्या है?",
        "opt_a": "sp", "opt_b": "sp2", "opt_c": "sp3", "opt_d": "dsp2",
        "correct_opt": "C",
        "explanation": "H2O में ऑक्सीजन के पास 2 बंध युग्म (Bond pairs) और 2 एकाकी युग्म (Lone pairs) होते हैं, अतः स्टिरिक संख्या 4 होने के कारण संकरण sp3 होता है (आकृति: मुड़ी हुई / Bent)।",
        "hint": "ऑक्सीजन के 2 बॉन्ड और 2 लोन पेयर गिने जाते हैं।"
    },
    {
        "subject": "chemistry", "topic": "chem_organic", "exam_level": "osssc", "language": "or",
        "question_text": "ବାୟୋଗ୍ୟାସ୍ କିମ୍ବା ଗୋବର ଗ୍ୟାସର ମୁଖ୍ୟ ଉପାଦାନ କ’ଣ?",
        "opt_a": "ବ୍ୟୁଟେନ୍", "opt_b": "ମିଥେନ୍ (Methane)", "opt_c": "ପ୍ରୋପେନ୍", "opt_d": "ଇଥାଇଲିନ୍",
        "correct_opt": "B",
        "explanation": "ବାୟୋଗ୍ୟାସରେ ପ୍ରାୟ ୫୫% ରୁ ୭୦% ମିଥେନ୍ (CH4) ଗ୍ୟାସ ଥାଏ, ଯାହା ମୁଖ୍ୟ ପ୍ରଜ୍ଜ୍ୱଳନଶୀଳ ଉପାଦାନ ଅଟେ।",
        "hint": "ଏହାର ରାସାୟନିକ ସୂତ୍ର ହେଉଛି CH4।"
    },
    {
        "subject": "chemistry", "topic": "chem_solutions", "exam_level": "12th", "language": "hinglish",
        "question_text": "Pure water ka pH 25°C par 7 hota hai. Agar temperature badha diya jaye, toh neutral water ka pH kya hoga?",
        "opt_a": "Badh jayega (>7)", "opt_b": "Kam ho jayega (<7)", "opt_c": "7 hi rahega", "opt_d": "14 ho jayega",
        "correct_opt": "B",
        "explanation": "Water ka dissociation endothermic reaction hai. Temperature badhane se Kw badhta hai aur H+ concentration badhne se pH ki numerical value 7 se kam ho jati hai (halanki pani neutral hi rehta hai kyunki [H+]=[OH-]).",
        "hint": "Kw temperature ke direct proportion mein badhta hai."
    },

    # ==========================
    # 📐 MATHEMATICS (ENGLISH, HINDI, ODIA, HINGLISH)
    # ==========================
    {
        "subject": "math", "topic": "math_num_sys", "exam_level": "ssc", "language": "en",
        "question_text": "What is the unit digit in the product: (7^95 - 3^58)?",
        "opt_a": "0", "opt_b": "4", "opt_c": "6", "opt_d": "7",
        "correct_opt": "B",
        "explanation": "Cyclicity of 7 is 4: 95 mod 4 = 3, so unit digit of 7^95 is 7^3 = 343 -> 3. Cyclicity of 3 is 4: 58 mod 4 = 2, so 3^2 = 9. Unit digit: (13 - 9) = 4.",
        "hint": "Find the cyclicity of base numbers 7 and 3, which is 4."
    },
    {
        "subject": "math", "topic": "math_trigo", "exam_level": "10th", "language": "hi",
        "question_text": "यदि sin θ = 3/5 है, तो (tan θ + sec θ) का मान क्या होगा?",
        "opt_a": "1", "opt_b": "2", "opt_c": "3", "opt_d": "4/3",
        "correct_opt": "B",
        "explanation": "sin θ = 3/5 (लम्ब=3, कर्ण=5, आधार=4)। अतः tan θ = 3/4 तथा sec θ = 5/4। मान = (3/4 + 5/4) = 8/4 = 2।",
        "hint": "पाइथागोरस त्रिक (3, 4, 5) का प्रयोग करें।"
    },
    {
        "subject": "math", "topic": "math_algebra", "exam_level": "osssc", "language": "or",
        "question_text": "ଗୋଟିଏ ଆୟତକ୍ଷେତ୍ରର ଦୈର୍ଘ୍ୟ ୨୦% ବୃଦ୍ଧି ଏବଂ ପ୍ରସ୍ଥ ୧୦% ହ୍ରାସ କରାଗଲେ, ଏହାର କ୍ଷେତ୍ରଫଳରେ କେତେ ଶତକଡ଼ା ପରିବର୍ତ୍ତନ ହେବ?",
        "opt_a": "୮% ବୃଦ୍ଧି", "opt_b": "୧୦% ହ୍ରାସ", "opt_c": "୫% ବୃଦ୍ଧି", "opt_d": "କୌଣସି ପରିବର୍ତ୍ତନ ହେବ ନାହିଁ",
        "correct_opt": "A",
        "explanation": "ଶତକଡ଼ା ପରିବର୍ତ୍ତନ = x + y + (xy/100) = 20 - 10 + (20 * -10 / 100) = 10 - 2 = +8% (ଅର୍ଥାତ୍ ୮% ବୃଦ୍ଧି)।",
        "hint": "ନିଟ୍ ଶତକଡ଼ା ସୂତ୍ର [x + y + xy/100] ପ୍ରୟୋଗ କରନ୍ତୁ।"
    },
    {
        "subject": "math", "topic": "math_num_sys", "exam_level": "ssc", "language": "hinglish",
        "question_text": "Agar do numbers ka HCF 12 hai aur unka LCM 144 hai, aur unme se ek number 36 hai, toh doosra number kya hoga?",
        "opt_a": "24", "opt_b": "48", "opt_c": "60", "opt_d": "72",
        "correct_opt": "B",
        "explanation": "Formula: First Number * Second Number = HCF * LCM. Isliye, 36 * N = 12 * 144 => N = (12 * 144) / 36 = 48.",
        "hint": "Product of two numbers = LCM * HCF."
    },

    # ==========================
    # 📜 HISTORY (ENGLISH, HINDI, ODIA, HINGLISH)
    # ==========================
    {
        "subject": "history", "topic": "hist_modern", "exam_level": "upsc", "language": "en",
        "question_text": "Who among the following presided over the historic 1929 Lahore Session of the Indian National Congress where 'Purna Swaraj' was declared?",
        "opt_a": "Mahatma Gandhi", "opt_b": "Jawaharlal Nehru", "opt_c": "Subhash Chandra Bose", "opt_d": "Sardar Vallabhbhai Patel",
        "correct_opt": "B",
        "explanation": "Jawaharlal Nehru presided over the Lahore Session in December 1929 where the resolution for 'Purna Swaraj' (Complete Independence) was passed, and January 26, 1930 was designated as Independence Day.",
        "hint": "He unfurled the tricolour on the banks of the Ravi River."
    },
    {
        "subject": "history", "topic": "hist_odisha", "exam_level": "opsc", "language": "en",
        "question_text": "The famous 'Paika Rebellion' of 1817 against the British colonial rule in Odisha was led by:",
        "opt_a": "Surendra Sai", "opt_b": "Bakshi Jagabandhu Bidyadhara", "opt_c": "Chakhi Khuntia", "opt_d": "Dharani Dhar",
        "correct_opt": "B",
        "explanation": "Bakshi Jagabandhu Bidyadhara Mohapatra was the commander of the militia of the King of Khurda who led the valiant Paika Bidroha in 1817 against oppressive British revenue and salt policies.",
        "hint": "He was the military chief (Senapati) of the King of Khurda."
    },
    {
        "subject": "history", "topic": "hist_odisha", "exam_level": "osssc", "language": "or",
        "question_text": "୧୮୧୭ ମସିହାରେ ଓଡ଼ିଶାର ଐତିହାସିକ 'ପାଇକ ବିଦ୍ରୋହ'ର ମୁଖ୍ୟ ନେତୃତ୍ୱ କିଏ ନେଇଥିଲେ?",
        "opt_a": "ବୀର ସୁରେନ୍ଦ୍ର ସାଏ", "opt_b": "ବକ୍ସି ଜଗବନ୍ଧୁ ବିଦ୍ୟାଧର", "opt_c": "ମାଧବ ଚନ୍ଦ୍ର ରାଉତରାୟ", "opt_d": "ଚାଖି ଖୁଣ୍ଟିଆ",
        "correct_opt": "B",
        "explanation": "ବକ୍ସି ଜଗବନ୍ଧୁ ଖୋର୍ଦ୍ଧା ରାଜାଙ୍କର ମୁଖ୍ୟ ସେନାପତି ଥିଲେ ଏବଂ ୧୮୧୭ ମସିହାରେ ଇଂରେଜ ମାନଙ୍କ ବିରୁଦ୍ଧରେ ସଶସ୍ତ୍ର ପାଇକ ବିଦ୍ରୋହର ନେତୃତ୍ୱ ନେଇଥିଲେ।",
        "hint": "ସେ ଖୋର୍ଦ୍ଧା ରାଜ୍ୟର ବଳିଷ୍ଠ ସେନାପତି ଥିଲେ।"
    },
    {
        "subject": "history", "topic": "hist_ancient", "exam_level": "ssc", "language": "hi",
        "question_text": "सिंधु घाटी सभ्यता का प्रसिद्ध 'विशाल स्नानागार' (Great Bath) किस स्थान पर पाया गया है?",
        "opt_a": "हड़प्पा", "opt_b": "लोथल", "opt_c": "मोहनजोदड़ो", "opt_d": "कालीबंगन",
        "correct_opt": "C",
        "explanation": "विशाल स्नानागार (The Great Bath) मोहनजोदड़ो (सिंध, पाकिस्तान) में खोजा गया था, जिसका उपयोग धार्मिक एवं सार्वजनिक अनुष्ठानिक स्नान के लिए किया जाता था।",
        "hint": "इस स्थल के नाम का अर्थ 'मृतकों का टीला' (Mound of the Dead) है।"
    },

    # ==========================
    # 🏛️ ODIA LANGUAGE & GRAMMAR (ଓଡ଼ିଆ)
    # ==========================
    {
        "subject": "odia", "topic": "odia_sandhi", "exam_level": "osssc", "language": "or",
        "question_text": "'ଗାୟକ' ଶବ୍ଦର ସଠିକ୍ ସନ୍ଧି ବିଚ୍ଛେଦ କ’ଣ ହେବ?",
        "opt_a": "ଗା + ଅକ", "opt_b": "ଗୈ + ଅକ", "opt_c": "ଗେ + ଅକ", "opt_d": "ଗାୟ + କ",
        "correct_opt": "B",
        "explanation": "ସ୍ୱରସନ୍ଧିର ନିୟମାନୁସାରେ, 'ଐ' କାର ପରେ ଅନ୍ୟ ସ୍ୱରବର୍ଣ୍ଣ ରହିଲେ 'ଐ' ସ୍ଥାନରେ 'ଆୟ' ହୁଏ। ତେଣୁ 'ଗୈ + ଅକ = ଗାୟକ'।",
        "hint": "ନିୟମ: ଐ + ଅ = ଆୟ।"
    },
    {
        "subject": "odia", "topic": "odia_sahitya", "exam_level": "opsc", "language": "or",
        "question_text": "ଓଡ଼ିଆ ଭାଷାରେ 'ଆଦିକବି' ଭାବରେ କିଏ ପରିଚିତ?",
        "opt_a": "ଉପେନ୍ଦ୍ର ଭଞ୍ଜ", "opt_b": "ରାଧାନାଥ ରାୟ", "opt_c": "ଶାରଳା ଦାସ", "opt_d": "ଫକୀର ମୋହନ ସେନାପତି",
        "correct_opt": "C",
        "explanation": "ପଞ୍ଚଦଶ ଶତାବ୍ଦୀର ପ୍ରସିଦ୍ଧ କବି ଶାରଳା ଦାସଙ୍କୁ ଓଡ଼ିଆ ଭାଷାର 'ଆଦିକବି' କୁହାଯାଏ, ଯିଏ ଓଡ଼ିଆ ମହାଭାରତ, ବିଳଙ୍କା ରାମାୟଣ ଓ ଚଣ୍ଡୀପୁରାଣ ରଚନା କରିଥିଲେ।",
        "hint": "ସେ ମହାଭାରତର ପ୍ରଥମ ଓଡ଼ିଆ ଅନୁବାଦକ।"
    },
    {
        "subject": "odia", "topic": "odia_shabda", "exam_level": "ossc", "language": "or",
        "question_text": "'ଅନ୍ଧାର ଘରେ ବାଡ଼ି ବୁଲାଇବା' - ଏହି ରୂଢ଼ିଟିର ପ୍ରକୃତ ଅର୍ଥ କ’ଣ?",
        "opt_a": "ରାତିରେ ଯାତ୍ରା କରିବା", "opt_b": "ଅନୁମାନରେ କାର୍ଯ୍ୟ କରିବା", "opt_c": "ଭୟଭୀତ ହେବା", "opt_d": "ଅସହାୟ ହୋଇପଡ଼ିବା",
        "correct_opt": "B",
        "explanation": "‘ଅନ୍ଧାର ଘରେ ବାଡ଼ି ବୁଲାଇବା’ ରୂଢ଼ିର ପ୍ରକୃତ ପ୍ରୟୋଗ ହେଉଛି କୌଣସି ନିର୍ଦ୍ଦିଷ୍ଟ ପ୍ରମାଣ ନଥାଇ କେବଳ ଅନୁମାନ କିମ୍ବା ଅନ୍ଧାରରେ ଢେଲା ଫିଙ୍ଗିବା ଭଳି କାମ କରିବା।",
        "hint": "ଏହା ଅନିଶ୍ଚିତତା କିମ୍ବା ବିନା ନିର୍ଦ୍ଦେଶରେ ଚେଷ୍ଟା କରିବାକୁ ବୁଝାଏ।"
    },

    # ==========================
    # 🧩 REASONING (ENGLISH, HINDI, ODIA, HINGLISH)
    # ==========================
    {
        "subject": "reasoning", "topic": "reas_coding", "exam_level": "ssc", "language": "en",
        "question_text": "In a certain code language, if 'DELHI' is coded as '73541' and 'CALCUTTA' is coded as '82589662', how will 'CALICUT' be coded?",
        "opt_a": "5279431", "opt_b": "8251896", "opt_c": "8251896", "opt_d": "8251896",
        "correct_opt": "B",
        "explanation": "Direct letter substitution code: C=8, A=2, L=5, I=1, C=8, U=9, T=6. Combining these gives 8251896.",
        "hint": "Look up each letter's assigned digit from DELHI and CALCUTTA directly."
    },
    {
        "subject": "reasoning", "topic": "reas_blood", "exam_level": "ssc", "language": "hi",
        "question_text": "एक तस्वीर की ओर इशारा करते हुए रमेश ने कहा, 'वह मेरे दादाजी के इकलौते पुत्र की पुत्री है।' उस लड़की का रमेश से क्या संबंध है?",
        "opt_a": "माता", "opt_b": "बहन", "opt_c": "चाची", "opt_d": "पुत्री",
        "correct_opt": "B",
        "explanation": "दादाजी का इकलौता पुत्र = रमेश के पिता। पिता की पुत्री = रमेश की बहन। अतः वह लड़की रमेश की बहन है।",
        "hint": "दादाजी के इकलौते पुत्र यानी खुद के पिता।"
    },
    {
        "subject": "reasoning", "topic": "reas_analogy", "exam_level": "osssc", "language": "or",
        "question_text": "ଯଦି 'ଓଡ଼ିଶା : ଭୁବନେଶ୍ୱର' ହୁଏ, ତେବେ 'ଆସାମ : ?' କ’ଣ ହେବ?",
        "opt_a": "ଗୁଆହାଟୀ", "opt_b": "ଦିସପୁର (Dispur)", "opt_c": "ଶିଲଂ", "opt_d": "ଇମ୍ଫାଲ",
        "correct_opt": "B",
        "explanation": "ଓଡ଼ିଶାର ରାଜଧାନୀ ଭୁବନେଶ୍ୱର ହୋଇଥିବା ପରି ଆସାମର ରାଜଧାନୀ ହେଉଛି ଦିସପୁର।",
        "hint": "ରାଜ୍ୟ ଏବଂ ସେମାନଙ୍କର ରାଜଧାନୀ ସମ୍ପର୍କ।"
    },

    # ==========================
    # 📖 ENGLISH (ENGLISH & HINGLISH)
    # ==========================
    {
        "subject": "english", "topic": "eng_vocab", "exam_level": "ssc", "language": "en",
        "question_text": "Select the most appropriate SYNONYM of the given word: 'CANDID'",
        "opt_a": "Deceitful", "opt_b": "Frank / Honest", "opt_c": "Arrogant", "opt_d": "Shy",
        "correct_opt": "B",
        "explanation": "'Candid' means truthful, straightforward, and sincere in speech (frank). 'Deceitful' is its antonym.",
        "hint": "Think of a candid photograph—unposed, natural, and honest."
    },
    {
        "subject": "english", "topic": "eng_grammar", "exam_level": "ossc", "language": "en",
        "question_text": "Choose the correct preposition: 'She has been studying in this college ________ 2021.'",
        "opt_a": "for", "opt_b": "since", "opt_c": "from", "opt_d": "by",
        "correct_opt": "B",
        "explanation": "In Present Perfect Continuous tense, 'since' is used for a specific starting point in time (2021), whereas 'for' is used for a duration or period of time.",
        "hint": "A definite year indicates a point of time, not a duration."
    },
    {
        "subject": "english", "topic": "eng_idioms", "exam_level": "ssc", "language": "hinglish",
        "question_text": "Idiom 'Once in a blue moon' ka correct meaning kya hai?",
        "opt_a": "Roz hone wali ghatna", "opt_b": "Bahut hi rare / kabhi-kabaar", "opt_c": "Purnima ki raat", "opt_d": "Khushi ka din",
        "correct_opt": "B",
        "explanation": "'Once in a blue moon' ka matlab hota hai extremely rare event jo bohot hi kam dekhne ko milta hai.",
        "hint": "Something that happens almost never."
    },

    # ==========================
    # 🌍 CURRENT AFFAIRS (ENGLISH, HINDI, ODIA, HINGLISH)
    # ==========================
    {
        "subject": "current_affairs", "topic": "ca_sports", "exam_level": "upsc", "language": "en",
        "question_text": "Which nation hosted the ICC Men's Cricket World Cup 2023 in its entirety?",
        "opt_a": "Australia", "opt_b": "India", "opt_c": "England", "opt_d": "South Africa",
        "correct_opt": "B",
        "explanation": "India hosted the entire ICC Men's Cricket World Cup 2023 across 10 venues from October 5 to November 19, 2023.",
        "hint": "The grand finale was held at the Narendra Modi Stadium in Ahmedabad."
    },
    {
        "subject": "current_affairs", "topic": "ca_odisha", "exam_level": "opsc", "language": "or",
        "question_text": "ଓଡ଼ିଶାର କେଉଁ ସ୍ଥାନରେ ଦେଶର ସର୍ବବୃହତ ହକି ଷ୍ଟାଡିୟମ୍ 'ବିର୍ସା ମୁଣ୍ଡା ଅନ୍ତର୍ଜାତୀୟ ହକି ଷ୍ଟାଡିୟମ୍' ନିର୍ମିତ ହୋଇଛି?",
        "opt_a": "ଭୁବନେଶ୍ୱର", "opt_b": "କଟକ", "opt_c": "ରାଉରକେଲା", "opt_d": "ସମ୍ବଲପୁର",
        "correct_opt": "C",
        "explanation": "ସୁନ୍ଦରଗଡ଼ ଜିଲ୍ଲାର ରାଉରକେଲାଠାରେ ୨୦୨୩ ପୁରୁଷ ହକି ବିଶ୍ୱକପ୍ ପାଇଁ ୨୦,୦୦୦ ରୁ ଅଧିକ ଆସନ ବିଶିଷ୍ଟ ବିର୍ସା ମୁଣ୍ଡା ଅନ୍ତର୍ଜାତୀୟ ହକି ଷ୍ଟାଡିୟମ୍ ପ୍ରତିଷ୍ଠା କରାଯାଇଛି।",
        "hint": "ଏହା ଓଡ଼ିଶାର ଇସ୍ପାତ ସହର (Steel City) ରେ ଅବସ୍ଥିତ।"
    },
    {
        "subject": "current_affairs", "topic": "ca_science_def", "exam_level": "upsc", "language": "hi",
        "question_text": "इसरो (ISRO) के 'चंद्रयान-3' मिशन के लैंडर का नाम क्या था, जिसने चंद्रमा के दक्षिणी ध्रुव पर सफल लैंडिंग की?",
        "opt_a": "प्रज्ञान", "opt_b": "विक्रम", "opt_c": "ध्रुव", "opt_d": "आदित्य",
        "correct_opt": "B",
        "explanation": "चंद्रयान-3 के लैंडर का नाम 'विक्रम' (डॉ. विक्रम साराभाई के सम्मान में) तथा रोवर का नाम 'प्रज्ञान' था। यह 23 अगस्त 2023 को सफलतापूर्वक उतरा।",
        "hint": "रोवर का नाम प्रज्ञान था, जबकि लैंडर का नाम वैज्ञानिक विक्रम साराभाई पर था।"
    },
    {
        "subject": "current_affairs", "topic": "ca_national", "exam_level": "ssc", "language": "hinglish",
        "question_text": "India ke naye Parliament House (Sansad Bhavan) ka design kis architect ne taiyar kiya hai?",
        "opt_a": "Bimal Patel", "opt_b": "Edwin Lutyens", "opt_c": "Hafeez Contractor", "opt_d": "Charles Correa",
        "correct_opt": "A",
        "explanation": "Naye Sansad Bhavan ka design mashhoor architect Dr. Bimal Patel (HCP Designs) ne Central Vista redevelopment project ke under taiyar kiya hai.",
        "hint": "Unhone Kashi Vishwanath corridor ka bhi design kiya tha."
    }
]

def seed_database_if_empty():
    """Seeds the question bank with rich competitive exam questions if questions table is empty."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS count FROM questions")
        count = cursor.fetchone()["count"]
        
        if count == 0:
            logger.info("Questions table is empty. Seeding initial questions...")
            for q in SEED_QUESTIONS:
                cursor.execute("""
                    INSERT INTO questions 
                    (subject, topic, exam_level, language, question_text, opt_a, opt_b, opt_c, opt_d, correct_opt, explanation, hint)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    q["subject"], q["topic"], q["exam_level"], q["language"],
                    q["question_text"], q["opt_a"], q["opt_b"], q["opt_c"], q["opt_d"],
                    q["correct_opt"], q["explanation"], q["hint"]
                ))
            conn.commit()
            logger.info(f"Successfully seeded {len(SEED_QUESTIONS)} high-yield exam questions.")
        else:
            logger.info(f"Database already contains {count} questions. Skipping seed.")

if __name__ == "__main__":
    from database import init_db
    init_db()
    seed_database_if_empty()
    print("Seed complete!")
