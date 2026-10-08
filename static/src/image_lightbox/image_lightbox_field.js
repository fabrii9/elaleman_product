import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useFileViewer } from "@web/core/file_viewer/file_viewer_hook";
import { ImageField, imageField } from "@web/views/fields/image/image_field";

/**
 * Imagen que se abre en grande (visor de Odoo, con zoom y descarga) al hacer clic.
 * Muestra siempre el campo completo (image_1920), no la miniatura del formulario.
 */
export class ImageLightboxField extends ImageField {
    static template = "elaleman_product.ImageLightboxField";

    setup() {
        super.setup();
        this.fileViewer = useFileViewer();
    }

    get canOpenLightbox() {
        return Boolean(this.props.record.data[this.props.name]) && this.state.isValid;
    }

    onImageClick() {
        if (!this.canOpenLightbox) {
            return;
        }
        const source = this.getUrl(this.props.name);
        const downloadUrl = source.startsWith("data:")
            ? source
            : `${source}${source.includes("?") ? "&" : "?"}download=true`;
        this.fileViewer.open({
            displayName: this.props.record.data.display_name || _t("Imagen"),
            defaultSource: source,
            downloadUrl,
            mimetype: "image/webp",
            isImage: true,
            isViewable: true,
        });
    }
}

export const imageLightboxField = {
    ...imageField,
    component: ImageLightboxField,
};

registry.category("fields").add("image_lightbox", imageLightboxField);
