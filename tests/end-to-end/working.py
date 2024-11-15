from werkzeug.security import generate_password_hash

simon_password = (generate_password_hash('LovelyBoy99'))
coco_password = (generate_password_hash('Princess99'))

print(simon_password, coco_password)
