import { onWillDestroy, useEffect } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { FileViewer } from "@web/core/file_viewer/file_viewer";
import { ImageField, imageField } from "@web/views/fields/image/image_field";

const mainComponents = registry.category("main_components");
let nextViewerId = 1;

/**
 * Imagen que se abre en grande (visor de Odoo, con zoom y descarga) al hacer clic.
 * Muestra siempre el campo completo (image_1920), no la miniatura del formulario.
 * Si el visor está abierto y se cambia de registro (paginado), muestra la imagen
 * del registro nuevo, o se cierra si no tiene.
 */
export class ImageLightboxField extends ImageField {
    static template = "elaleman_product.ImageLightboxField";

    setup() {
        super.setup();
        this.viewerKey = null;
        onWillDestroy(() => this.closeLightbox());
        useEffect(
            () => {
                if (this.isLightboxOpen) {
                    if (this.canOpenLightbox) {
                        this.openLightbox();
                    } else {
                        this.closeLightbox();
                    }
                }
            },
            () => [this.props.record.resId, this.props.record.data[this.props.name]]
        );
    }

    get canOpenLightbox() {
        return Boolean(this.props.record.data[this.props.name]) && this.state.isValid;
    }

    get isLightboxOpen() {
        return Boolean(this.viewerKey) && mainComponents.contains(this.viewerKey);
    }

    onImageClick() {
        if (this.canOpenLightbox) {
            this.openLightbox();
        }
    }

    openLightbox() {
        this.closeLightbox();
        const source = this.getUrl(this.props.name);
        const downloadUrl = source.startsWith("data:")
            ? source
            : `${source}${source.includes("?") ? "&" : "?"}download=true`;
        const file = {
            displayName: this.props.record.data.display_name || _t("Imagen"),
            defaultSource: source,
            downloadUrl,
            mimetype: "image/webp",
            isImage: true,
            isViewable: true,
        };
        // Clave nueva en cada apertura: el visor guarda el archivo en su estado
        // interno, así que reutilizar la clave mostraría la imagen anterior.
        const key = `elaleman_product.image_lightbox_${nextViewerId++}`;
        this.viewerKey = key;
        mainComponents.add(key, {
            Component: FileViewer,
            props: { files: [file], startIndex: 0, close: () => this.closeLightbox(key) },
        });
    }

    closeLightbox(key = this.viewerKey) {
        if (key && mainComponents.contains(key)) {
            mainComponents.remove(key);
        }
        if (key === this.viewerKey) {
            this.viewerKey = null;
        }
    }
}

export const imageLightboxField = {
    ...imageField,
    component: ImageLightboxField,
};

registry.category("fields").add("image_lightbox", imageLightboxField);
