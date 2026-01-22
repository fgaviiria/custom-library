FROM odoo:18.0

COPY ./library_management /mnt/extra-addons/library_management
COPY ./odoo.conf /etc/odoo/odoo.conf

USER root
RUN chown -R odoo /mnt/extra-addons
USER odoo
